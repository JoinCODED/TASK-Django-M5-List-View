from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Flight


class FlightListTest(APITestCase):
    def setUp(self):
        self.flight1 = {
            "destination": "Wakanda",
            "time": "10:00",
            "price": 230,
            "miles": 4000,
        }
        self.flight2 = {
            "destination": "La la land",
            "time": "00:00",
            "price": 1010,
            "miles": 1010,
        }
        Flight.objects.create(**self.flight1)
        Flight.objects.create(**self.flight2)

    def test_url_works(self):
        response = self.client.get(reverse("flights-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        response = self.client.get(reverse("flights-list"))
        flights = Flight.objects.all()
        self.assertEqual(len(response.data), flights.count())
        flight = flights[0]
        self.assertEqual(
            dict(response.data[0]),
            {
                "id": flight.id,
                "destination": flight.destination,
                "time": str(flight.time),
                "price": str(flight.price),
            },
        )
        flight = flights[1]
        self.assertEqual(
            dict(response.data[1]),
            {
                "id": flight.id,
                "destination": flight.destination,
                "time": str(flight.time),
                "price": str(flight.price),
            },
        )


class BookingListTest(APITestCase):
    def setUp(self):
        self.flight1 = {
            "destination": "Wakanda",
            "time": "10:00",
            "price": 230,
            "miles": 4000,
        }
        self.flight2 = {
            "destination": "La la land",
            "time": "00:00",
            "price": 1010,
            "miles": 1010,
        }
        flight1 = Flight.objects.create(**self.flight1)
        flight2 = Flight.objects.create(**self.flight2)
        user = User.objects.create(username="laila", password="1234567890-=")

        today = date.today()
        Booking.objects.create(
            flight=flight1,
            date=today.replace(year=today.year - 2, day=1),
            user=user,
            passengers=2,
        )
        Booking.objects.create(
            flight=flight2,
            date=today.replace(year=today.year - 1, day=1),
            user=user,
            passengers=2,
        )
        Booking.objects.create(
            flight=flight1,
            date=today.replace(year=today.year + 1, day=1),
            user=user,
            passengers=2,
        )
        Booking.objects.create(
            flight=flight2,
            date=today.replace(year=today.year + 1, day=1),
            user=user,
            passengers=2,
        )

    def test_url_works(self):
        response = self.client.get(reverse("bookings-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        response = self.client.get(reverse("bookings-list"))
        bookings = list(Booking.objects.filter(date__gt=date.today()))

        self.assertEqual(len(response.data), len(bookings))

        for actual, booking in zip(response.data, bookings):
            expected = {
                "id": booking.id,
                "flight": booking.flight.id,
                "date": str(booking.date),
            }
            self.assertEqual(actual, expected)
