from archive.models import Media, Tag, Condition,Item, Category, Address, Area, Room, Location #,Topic
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, RequestContext

from django.views.generic.list import ListView
from django.views.generic import DetailView
import pdb


class ItemListView(ListView):
	model = Item
	
	def get_queryset(self):
		if self.args and self.args[0]:
			c = get_object_or_404(Category, pk=self.args[0])
			self.parent_category = c
			self.child_categories = c.get_children()
			return(c.item_set.all())
		else:
			self.parent_category = None
			self.child_categories = Category.objects.root_nodes()
			return(Item.objects.filter(pk=None))
	
	def get_context_data(self, **kwargs):
		context = super(ItemListView, self).get_context_data(**kwargs)
		context['parent'] = self.parent_category
		context['nodes'] = self.child_categories
		return(context)

class ItemDetailView(DetailView):
	model = Item

@csrf_exempt
def image_details(request):
	if request.method == "GET":
		from archive.models import Media
		mpk = request.GET.get('media_pk') 
		m = Media.objects.get(pk=mpk)
		context = {}
		context['filename'] = m.filename.name 
		context['file'] = m.filename
		context['mime'] = m.media_type
		return render_to_response('archive/media_details.html', context,context_instance=RequestContext(request))

@csrf_exempt
def search(request):
	return render_to_response('archive/search.html', context_instance=RequestContext(request))



@csrf_exempt
def museum(request):
	page_items = {}
	if request.GET.has_key('node'):
		node_id = request.GET.get('node')
		c = Category.objects.get(pk=node_id)
		page_items['parent'] = c
		page_items['nodes'] = c.get_children()
		page_items['items'] = c.item_set.all()
	else:
		page_items['nodes'] = Category.objects.root_nodes()
		#No items since all items displayed must a connection to the chosen node.
		
	return render_to_response('archive/museum.html', page_items, context_instance=RequestContext(request))

#used
@csrf_exempt
def area_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				addr = Address.objects.filter(pk=value)
				models = Area.objects.filter(address=addr)
				results = [(t.pk, t.name) for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

#used
@csrf_exempt
def room_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				area = Area.objects.get(pk=value)
				models = Room.objects.filter(area=area)
				results = [(t.pk, t.name) for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

#used
@csrf_exempt
def location_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			if value:
				room = Room.objects.get(pk=value)
				models = Location.objects.filter(room=room)
				results = [(t.pk, t.name) for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

@csrf_exempt
def tag_autocomplete(request):
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Tag.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json) #, mimetype='application/json')

@csrf_exempt
def keyword_autocomplete(request):
	from archive.models import Keywords
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Keywords.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

@csrf_exempt
def material_autocomplete(request):
	from archive.models import Materials
	results = []
	if request.method == "POST":
		if request.POST.has_key(u'query'):
			value = request.POST.get(u'query')
			models = Materials.objects.filter(name__icontains=value)
			results = [t.name for t in models]
	json = simplejson.dumps(results)
	return HttpResponse(json)

#@csrf_exempt
#def topic_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'topic'):
#			value = request.POST.get(u'topic')
#			models = Topic.objects.filter(topic__icontains=value)
#			results = [t.topic for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#
#@csrf_exempt
#def room_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'area'):
#			value = request.POST.get(u'area')
#			models = Location.objects.filter(area__iexact=value)
#			results = [t.room for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#@csrf_exempt
#def subtopic_autocomplete(request):
#	results = []
#	if request.method == "POST":
#		if request.POST.has_key(u'topic') and request.POST.has_key(u'subtopic'):
#			topic = request.POST.get(u'topic')
#			subtopic = request.POST.get(u'subtopic')
#			models = Topic.objects.filter(topic__iexact=topic).filter(subtopic__icontains=subtopic)
#			results = [t.subtopic for t in models]
#	json = simplejson.dumps(results)
#	return HttpResponse(json)
#
#def add_location(request):
#	response = HttpResponse()
#	response['Content-Type'] = 'application/json'
#	
#	if request.method == "POST":
#		form = LocationEditForm(request.POST)
#		if form.is_valid():
#			form.save()
#			
#			response.write(simplejson.dumps("OK"))
#		else:
#			response.write(simplejson.dumps("FAIL: " + "\n" + "\n".join(form.errors.keys())))
#	else:
#		response.write("Not a POST")
#		#return HttpResponse("FAIL")
#	
#	return(response)

