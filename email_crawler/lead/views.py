import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import LeadSerializer
from .models import Lead
from .utils import SCOPES, crawler_pipeline


class LeadViewSet(viewsets.ModelViewSet):

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    @action(detail=False, methods=['get'])
    def search_leads(self, request):
        from_email = request.query_params.get('from')
        subject = request.query_params.get('subject')

        credentials = None
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'token.pickle')

        try:
            with open(file_path, 'rb') as token:
                credentials = pickle.load(token)

        except FileNotFoundError:
            return Response(
                {'detail': 'credentials not found in our server'},
                status.HTTP_404_NOT_FOUND
            )

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and \
               credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credentials = flow.run_local_server()

            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        service = build('gmail', 'v1', credentials=credentials)

        query_string = 'from:arturbersan@gmail.com subject:Consulta para o imóvel'
        if from_email or subject:
            query_string = 'from:{} subject:{}'.format(
                from_email or 'arturbersan@gmail.com',
                subject or 'Consulta para o imóvel'
            )

        results = service.users().messages().list(
            userId='me', q=query_string).execute()

        leads = []
        status_code = status.HTTP_200_OK
        if len(results.get('messages', [])) > 0:
            id_list = [x.get('id') for x in results.get('messages')]
            leads = crawler_pipeline(service, id_list)

            if len(leads) > 0:
                serialized_data = self.serializer_class(data=leads, many=True)
                serialized_data.is_valid(raise_exception=True)
                serialized_data.save()
        else:
            status_code = status.HTTP_404_NOT_FOUND

        return Response(
            {'detail': 'found {} leads'.format(len(leads))},
            status_code
        )
