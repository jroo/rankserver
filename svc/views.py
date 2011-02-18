from svc.models import Campaign, CampaignOption, FormSubmission
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
import uuid

def _get_by_external_id(external_id):
    campaigns = Campaign.objects.filter(external_id=external_id)
    if len(campaigns) > 0:
        campaign = campaigns[0]
    else:
        campaign = None
    return campaign

def campaign(request):
    id = request.GET['id']
    campaigns = Campaign.objects.filter(external_id=id)
    if len(campaigns) > 0:
        campaign = campaigns[0]
    else:
        campaign = None
    print id
    r = render_to_response('svc/campaign.json', {'campaign': campaign})
    r.mimetype = "application/json"
    return r
    
def results(request, format):
    resultset = []
    campaign = _get_by_external_id(request.GET['id'])  
    points = FormSubmission.objects.values('item_id').annotate(total_points=Sum('points')).filter(campaign=campaign).order_by('-total_points')
    first_place = FormSubmission.objects.values('item_id').annotate(fp_votes=Count('points')).filter(campaign=campaign).filter(rank=1).order_by('-fp_votes')
    
    scale = float(100)/float(points[0]['total_points'])
    
    for i in points:
        item = CampaignOption.objects.get(pk=i['item_id'])
        first_place_votes = 0
        for j in first_place:
            if j['item_id'] == i['item_id']:
                first_place_votes = j['fp_votes']
                
        result_item = {}
        result_item['id'] = item.id
        result_item['title'] = item.title
        result_item['description'] = item.description
        result_item['rank'] = 1
        result_item['points'] = i['total_points']
        result_item['scaled'] = int(i['total_points'] * scale)
        result_item['first_place_votes'] = first_place_votes
        
        resultset.append(result_item)
        
        result_dict = {'id':campaign.id, 'external_id':campaign.external_id, 'title':campaign.title, 'items':resultset}

    mime = 'text/html'
    if format == 'json':
        mime = 'application/json'
    
    r = render_to_response('svc/results.%s' % format, {'results':result_dict})
    r.mimetype = mime
    return r
    
@csrf_exempt
def submit(request):
    
    def _convert_to_points(campaign, rank):
        rank = int(rank)
        multiplier = int(campaign.multiplier)
        max_options = int(campaign.max_options)
        return (max_options - rank + 1) * multiplier
        
    if request.POST:   
        submission_id = uuid.uuid4()
        campaign = Campaign.objects.get(pk=int(request.POST['id']))
        for k,v in request.POST.items():
            if k.split('_')[0] == 'item':
                item_id = int(k.split('_')[1])
                item_value = v
                fs = FormSubmission()
                fs.campaign = campaign
                fs.submission_id = submission_id
                fs.item = CampaignOption.objects.get(pk=item_id)
                fs.rank = item_value
                fs.points = _convert_to_points(fs.campaign, fs.rank)
                fs.save()
            
        if request.is_ajax():
            format = 'json'
        else:
            format = 'html'
        return HttpResponseRedirect('/results.%s?id=%s' % (format, campaign.external_id))

    else:
        return HttpResponseNotFound("not found")