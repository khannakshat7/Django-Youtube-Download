from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from pytube import YouTube
from pytube import Stream
from django.template.defaultfilters import filesizeformat


from .forms import urlform
# Create your views here.
yt = None
def urlcheck(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = urlform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            video_url = form.cleaned_data.get("url")
            if 'm.' in video_url:
                video_url = video_url.replace(u'm.', u'')

            elif 'youtu.be' in video_url:
                video_id = video_url.split('/')[-1]
                video_url = 'https://www.youtube.com/watch?v=' + video_id
        
            if len(video_url.split("=")[-1]) != 11:
                return HttpResponse('Enter correct url.')

            global yt
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(type="audio").order_by("abr").all()
            video_stream_720 = yt.streams.filter(res = "720p").all()
            video_stream_480 = yt.streams.filter(res = "480p").all()
            video_stream_360 = yt.streams.filter(res = "360p").all()
            video_stream_240 = yt.streams.filter(res = "240p").all()
            video_stream_144 = yt.streams.filter(res = "144p").all()

            context = {
            'form': form,
            'title': yt.title,
            'video_url': video_url,
            'description': yt.description,
            'views': yt.views,
            'streams': yt.streams.all(),
            'audio_stream': audio_stream,
            'video_stream_720': video_stream_720,
            'video_stream_480': video_stream_480,
            'video_stream_360': video_stream_360,
            'video_stream_240': video_stream_240,
            'video_stream_144': video_stream_144
            }

            return render(request, 'home.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = urlform()

    return render(request, 'home.html', { 'form': form })


def downloadvideo(request, viditag):
    form = urlform(request.POST)
    context = {}
    video = yt.streams.get_by_itag(viditag)
    video.download("media/")
    context['down'] = "../media/"+video.default_filename
    context['form'] = form
    return render(request, 'home.html',context)
