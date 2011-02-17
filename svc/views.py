from svc.models import Campaign, CampaignOption, FormSubmission
from django.http import HttpResponse
from django.shortcuts import render_to_response
import uuid

def campaign(request):
    id = request.GET['id']
    campaigns = Campaign.objects.filter(external_id=id)
    if len(campaigns) > 0:
        campaign = campaigns[0]
    else:
        campaign = None
    return render_to_response('svc/campaign.json', {'campaign': campaign})
    
def submit(request):
    
    def _convert_to_points(campaign, rank):
        print campaign.
        
    submission_id = uuid.uuid4()
    for k,v in request.POST.items():
        if k.split('_')[0] == 'item':
            item_id = int(k.split('_')[1])
            item_value = v
            fs = FormSubmission()
            fs.campaign = Campaign.objects.get(pk=int(request.POST['id']))
            fs.submission_id = submission_id
            fs.item = CampaignOption.objects.get(pk=item_id)
            fs.rank = item_value
            fs.points = convert_to_points(fs.campaign, fs.rank)
            fs.save()
            
    return HttpResponse('bloop')