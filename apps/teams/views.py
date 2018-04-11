from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (ManTeamMembers, ManTeamMatches, ManTeamMatchData,
                     WomanTeamMembers, WomanTeamMatches, WomanTeamMatchData)
from .serializers import (ManTeamMemberSerializer, ManTeamMatchSerializer, ManTeamMatchDataSerializer,
                          WomanTeamMemberSerializer, WomanTeamMatchSerializer, WomanTeamMatchDataSerializer)

