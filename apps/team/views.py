from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (ManTeamMember, ManTeamMatch, ManTeamMatchData,
                     WomanTeamMember, WomanTeamMatch, WomanTeamMatchData)
from .serializers import (ManTeamMemberSerializer, ManTeamMatchSerializer, ManTeamMatchDataSerializer,
                          WomanTeamMemberSerializer, WomanTeamMatchSerializer, WomanTeamMatchDataSerializer)

