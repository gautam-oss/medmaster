from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Conversation, Message
from .services import get_gemini_response


def chat_page(request):
    context = {}
    if request.user.is_authenticated:
        try:
            conversation = Conversation.objects.get(user=request.user)
            context['messages'] = conversation.messages.all()[:50]
        except Conversation.DoesNotExist:
            context['messages'] = []
    else:
        context['messages'] = []
        context['is_guest'] = True
    return render(request, 'chatbot/chat.html', context)


@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        if len(user_message) > 1000:
            return JsonResponse({'error': 'Message too long. Please limit to 1000 characters.'}, status=400)

        recent_messages = []

        if request.user.is_authenticated:
            conversation, _ = Conversation.objects.get_or_create(user=request.user)
            user_msg = Message.objects.create(conversation=conversation, content=user_message, is_from_user=True)
            recent_messages = conversation.messages.all()[:10]

        ai_response = get_gemini_response(user_message, recent_messages)

        if request.user.is_authenticated:
            ai_msg = Message.objects.create(conversation=conversation, content=ai_response, is_from_user=False)
            conversation.save()
            return JsonResponse({
                'success': True,
                'ai_response': ai_response,
                'user_message_id': user_msg.id,
                'ai_message_id': ai_msg.id,
                'is_authenticated': True,
            })
        else:
            return JsonResponse({
                'success': True,
                'ai_response': ai_response,
                'is_authenticated': False,
            })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong. Please try again.'}, status=500)
