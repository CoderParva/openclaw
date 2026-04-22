import json
import os
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .models import Chat, Message


def index(request):
    return render(request, 'index.html')


# ── CHAT CRUD ──

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


@csrf_exempt
def chat_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    body = json.loads(request.body or '{}')
    chat = Chat.objects.create(title=body.get('title', 'New Chat'))
    return JsonResponse({'id': str(chat.id), 'title': chat.title})


@csrf_exempt
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
        body = json.loads(request.body or '{}')
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


@csrf_exempt
def pin_message(request, message_id):
    try:
        msg = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    msg.pinned = not msg.pinned
    msg.save()
    return JsonResponse({'pinned': msg.pinned})


# ── GROQ STREAMING ──

@csrf_exempt
def chat_stream(request, chat_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    body = json.loads(request.body or '{}')
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

    def stream_response():
        import httpx
        full_response = ''
        try:
            with httpx.Client(timeout=60) as client:
                with client.stream(
                    'POST',
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json',
                    },
                    json={'model': model, 'messages': history, 'stream': True},
                ) as resp:
                    if resp.status_code == 429:
                        yield 'data: {"error":"rate_limit"}\n\n'
                        return
                    if resp.status_code == 401:
                        yield 'data: {"error":"invalid_key"}\n\n'
                        return
                    if resp.status_code != 200:
                        yield f'data: {{"error":"api_error","status":{resp.status_code}}}\n\n'
                        return
                    for line in resp.iter_lines():
                        if not line or not line.startswith('data:'):
                            continue
                        data = line[5:].strip()
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk['choices'][0]['delta'].get('content', '')
                            if delta:
                                full_response += delta
                                yield f'data: {json.dumps({"delta": delta})}\n\n'
                        except Exception:
                            continue
        except Exception as e:
            yield f'data: {{"error":"connection","detail":"{str(e)}"}}\n\n'
            return

        # Save AI response
        if full_response:
            Message.objects.create(chat=chat, role='assistant', content=full_response)
        yield 'data: [DONE]\n\n'

    response = StreamingHttpResponse(stream_response(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


# ── EXPORT ──

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

    from django.http import HttpResponse
    response = HttpResponse('\n'.join(lines), content_type='text/plain')
    filename = chat.title.lower().replace(' ', '-')[:30]
    response['Content-Disposition'] = f'attachment; filename="openclaw-{filename}.txt"'
    return response
