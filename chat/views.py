import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Chat, Message
import httpx


def index(request):
    return render(request, 'index.html')


def chat_list(request):
    chats = Chat.objects.all()
    data = [{
        'id': str(c.id),
        'title': c.title,
        'pinned': c.pinned,
        'updated_at': c.updated_at.isoformat(),
        'message_count': c.messages.count(),
    } for c in chats]
    return JsonResponse({'chats': data})


def chat_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body or '{}')
    except:
        body = {}
    chat = Chat.objects.create(title=body.get('title', 'New Chat'))
    return JsonResponse({'id': str(chat.id), 'title': chat.title})


def chat_detail(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        messages = [{
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'pinned': m.pinned,
            'created_at': m.created_at.isoformat(),
        } for m in chat.messages.all()]
        return JsonResponse({
            'id': str(chat.id),
            'title': chat.title,
            'pinned': chat.pinned,
            'messages': messages,
        })

    if request.method == 'PATCH':
        try:
            body = json.loads(request.body or '{}')
        except:
            body = {}
        if 'title' in body:
            chat.title = body['title']
        if 'pinned' in body:
            chat.pinned = body['pinned']
        chat.save()
        return JsonResponse({'id': str(chat.id), 'title': chat.title, 'pinned': chat.pinned})

    if request.method == 'DELETE':
        chat.delete()
        return JsonResponse({'deleted': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def pin_message(request, message_id):
    try:
        msg = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    msg.pinned = not msg.pinned
    msg.save()
    return JsonResponse({'pinned': msg.pinned})


def chat_stream(request, chat_id):
    """Non-streaming version — more reliable on free hosting"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        body = json.loads(request.body or '{}')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_message = body.get('message', '').strip()
    api_key = body.get('api_key', '').strip()
    model = body.get('model', 'llama3-70b-8192')

    if not user_message:
        return JsonResponse({'error': 'Message required'}, status=400)
    if not api_key:
        return JsonResponse({'error': 'API key required'}, status=400)

    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)

    # Save user message
    Message.objects.create(chat=chat, role='user', content=user_message)

    # Auto-title
    if chat.title == 'New Chat':
        chat.title = user_message[:40] + ('…' if len(user_message) > 40 else '')
        chat.save()

    # Build message history
    history = [
        {'role': 'system', 'content': 'You are a helpful, friendly, and smart AI assistant. Be clear, warm, and concise. Use markdown when helpful.'}
    ]
    for m in chat.messages.all():
        history.append({'role': m.role, 'content': m.content})

    # Call Groq API — NO streaming, simple response
    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': model,
                    'messages': history,
                    'stream': False,  # NO streaming
                }
            )

        if resp.status_code == 429:
            return JsonResponse({'error': 'rate_limit'}, status=429)
        if resp.status_code == 401:
            return JsonResponse({'error': 'invalid_key'}, status=401)
        if resp.status_code != 200:
            return JsonResponse({'error': f'api_error {resp.status_code}'}, status=500)

        data = resp.json()
        ai_message = data['choices'][0]['message']['content']

        # Save AI response
        msg = Message.objects.create(chat=chat, role='assistant', content=ai_message)

        return JsonResponse({
            'response': ai_message,
            'message_id': msg.id,
            'chat_title': chat.title,
            'message_count': chat.messages.count(),
        })

    except httpx.TimeoutException:
        return JsonResponse({'error': 'timeout'}, status=504)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def export_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    lines = [f'OpenClaw Export — {chat.title}', '=' * 50, '']
    for m in chat.messages.all():
        role = 'You' if m.role == 'user' else 'AI'
        lines.append(f'[{role} — {m.created_at.strftime("%Y-%m-%d %H:%M")}]')
        lines.append(m.content)
        lines.append('')

    response = HttpResponse('\n'.join(lines), content_type='text/plain')
    filename = chat.title.lower().replace(' ', '-')[:30]
    response['Content-Disposition'] = f'attachment; filename="openclaw-{filename}.txt"'
    return response
