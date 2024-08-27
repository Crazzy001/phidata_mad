from django.shortcuts import render, redirect

from phi.assistant import Assistant

def index(request):
    try:
        # Create a assistant
        assistant = Assistant()
        if 'messages' not in request.session:
            request.session['messages'] = []
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            # Add the prompt to the messages
            request.session['messages'].append({"role": "user", "content": prompt})
            # Set the session as modified
            request.session.modified = True
            # Create a response
            response = assistant.run(prompt, stream=False)
            # Append the response to the messages
            request.session['messages'].append({"role": "assistant", "content": response})
            # Set the session as modified
            request.session.modified = True
            # Redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
            }
            return render(request, 'chat/index.html', context)
        else:
            context = {
                'messages': request.session['messages'],
                'prompt': '',
            }
            return render(request, 'chat/index.html', context)
    except Exception as e:
        print(e)
        return redirect('index')


def new_chat(request):
    # -*- Clears the session messages and redirects to the home page -*-
    request.session.pop('assistant', None)
    request.session.pop('messages', None)
    return redirect('index')
