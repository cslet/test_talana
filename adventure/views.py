from ast import Try
from dis import dis
from statistics import mode
from urllib import response
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from adventure import models, notifiers, repositories, serializers, usecases
from django.db.models import Exists
from datetime import date


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        try:
            vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
            vehicle = models.Vehicle.objects.create(
                name=payload["name"],
                passengers=payload["passengers"],
                vehicle_type=vehicle_type,
            )
            return Response(
                {
                    "id": vehicle.id,
                    "name": vehicle.name,
                    "passengers": vehicle.passengers,
                    "vehicle_type": vehicle.vehicle_type.name,
                },
                status=201,
            )
        except Exception as e:
            return Response(
                {
                    "message": e
                },
                status=404
            )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()

class GetDistribution(APIView):
    def post(self, request: Request) -> Response:
            payload = request.data
            try:

                vehicle_type = models.Vehicle.objects.get(name='car')
                arrayBool = list()
                for i in range(1, (vehicle_type.passengers + 1)):
                    # print(i)
                    if ( i % 2 != 0 and i == vehicle_type.passengers):
                        arrayBool.append([True, False])
                        break
                    elif(i % 2) :
                        arrayBool.append([True, True])
                
                return Response(
                    {
                        "message": arrayBool
                    },
                    status=200
                )    
            except Exception as e:
                return Response(
                    {
                        "message": str(e)
                    },
                    status=404
                )    

class StopJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StopJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()       

class GetIsFinished(APIView):
    def post(self, request: Request) -> Response:
            payload = request.data
            vehicle_name = models.Vehicle.objects.get(name='car')
            vehicle = models.Journey(end=date.today(), vehicle=vehicle_name)
            # name = vehicle.name
            finalizado = vehicle.vehicle
            try:

                return Response(
                    {
                        "message": finalizado
                    },
                    status=200
                )    
            except Exception as e:
                return Response(
                    {
                        "message": str(e)
                    },
                    status=404
                )           