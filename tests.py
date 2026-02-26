from unittest.mock import patch

from django.http import JsonResponse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls.exceptions import Resolver404

from .middleware import ErrorHandlerMiddleware, LoginRequiredMiddleware
from .models import Laptops_records, Mobile_records, location_details
from .views import Laptops_data, Mobile_data, custom_404, custom_500


class LaptopRecordModelTest(TestCase):
    def test_create_laptop_record(self):
        record = Laptops_records.objects.create(
            Lapassetid="ASSET-001",
            LapSerialNo="SN-001",
            LapMake="Dell",
            LapModel="Latitude 5520",
            LapRAM="16",
            LapHDD="512 GB",
            LapProcessor="Intel i7",
            Lappurchasedate="2024-01-15",
            Lapuname="testuser",
        )
        self.assertEqual(record.Lapassetid, "ASSET-001")
        self.assertEqual(record.LapMake, "Dell")

    def test_create_laptop_record_without_purchase_date(self):
        record = Laptops_records.objects.create(
            Lapassetid="ASSET-002",
            LapSerialNo="SN-002",
            LapMake="HP",
            LapModel="EliteBook",
            LapRAM="8",
            LapHDD="256 GB",
            LapProcessor="Intel i5",
            Lapuname="testuser2",
        )
        self.assertIsNone(record.Lappurchasedate)


class MobileRecordModelTest(TestCase):
    def test_create_mobile_record(self):
        record = Mobile_records.objects.create(
            Mobassetid="MOB-001",
            MobSerialNo="MSN-001",
            imei_number="123456789012345",
            MobMake="Samsung",
            MobModel="Galaxy S23",
            Mobpurchasedate="2024-03-01",
            Mobuname="testuser",
        )
        self.assertEqual(record.Mobassetid, "MOB-001")
        self.assertEqual(record.imei_number, "123456789012345")


class LaptopsDataViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_get_request_rejected(self):
        request = self.factory.get('/Laptops_data/')
        request.user = self.user
        response = Laptops_data(request)
        self.assertEqual(response.status_code, 405)

    def test_post_missing_make_returns_error(self):
        request = self.factory.post('/Laptops_data/', {})
        request.user = self.user
        response = Laptops_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Make', response.content)

    def test_post_non_numeric_ram_returns_error(self):
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'Dell',
            'inputLapModel': 'Latitude',
            'inputLapRAM': 'abc',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertIn(b'RAM must be a number', response.content)

    def test_post_ram_too_high_returns_error(self):
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'Dell',
            'inputLapModel': 'Latitude',
            'inputLapRAM': '200',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertIn(b'RAM_Greater', response.content)

    def test_post_successful_laptop_creation(self):
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'Dell',
            'inputLapModel': 'Latitude',
            'inputLapRAM': '16',
            'inputLapHDDType': 'GB',
            'inputLapHDD': '512',
            'inputLapProcessor': 'Intel i7',
            'inputLappurchasedate': '2024-01-15',
            'inputLapSerialNo': 'SN-100',
            'inputLapassetid': 'ASSET-100',
            'inputLapuname': 'newuser',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertIn(b'success', response.content)
        self.assertTrue(Laptops_records.objects.filter(Lapassetid='ASSET-100').exists())

    def test_post_duplicate_asset_id_returns_exists(self):
        Laptops_records.objects.create(
            Lapassetid="ASSET-DUP",
            LapSerialNo="SN-DUP",
            LapMake="Dell",
            LapModel="Latitude",
            LapRAM="16",
            LapHDD="512 GB",
            LapProcessor="Intel i7",
            Lapuname="existinguser",
        )
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'HP',
            'inputLapModel': 'EliteBook',
            'inputLapRAM': '8',
            'inputLapHDDType': 'GB',
            'inputLapHDD': '256',
            'inputLapProcessor': 'Intel i5',
            'inputLapSerialNo': 'SN-NEW',
            'inputLapassetid': 'ASSET-DUP',
            'inputLapuname': 'newuser2',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertIn(b'exists', response.content)


class MobileDataViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_get_request_rejected(self):
        request = self.factory.get('/Mobile_data/')
        request.user = self.user
        response = Mobile_data(request)
        self.assertEqual(response.status_code, 405)

    def test_post_missing_make_returns_error(self):
        request = self.factory.post('/Mobile_data/', {})
        request.user = self.user
        response = Mobile_data(request)
        self.assertIn(b'Make', response.content)

    def test_post_successful_mobile_creation(self):
        request = self.factory.post('/Mobile_data/', {
            'inputMobMake': 'Samsung',
            'inputMobModel': 'Galaxy S23',
            'inputMobIMIE': '123456789012345',
            'inputMobpurchasedate': '2024-03-01',
            'inputMobSerialNo': 'MSN-100',
            'inputMobassetid': 'MOB-100',
            'inputMobuname': 'mobileuser',
        })
        request.user = self.user
        response = Mobile_data(request)
        self.assertIn(b'success', response.content)
        self.assertTrue(Mobile_records.objects.filter(Mobassetid='MOB-100').exists())

    def test_post_duplicate_imei_returns_exists(self):
        Mobile_records.objects.create(
            Mobassetid="MOB-DUP",
            MobSerialNo="MSN-DUP",
            imei_number="999999999999999",
            MobMake="Apple",
            MobModel="iPhone 15",
            Mobuname="existinguser",
        )
        request = self.factory.post('/Mobile_data/', {
            'inputMobMake': 'Samsung',
            'inputMobModel': 'Galaxy S24',
            'inputMobIMIE': '999999999999999',
            'inputMobSerialNo': 'MSN-NEW',
            'inputMobassetid': 'MOB-NEW',
            'inputMobuname': 'newuser',
        })
        request.user = self.user
        response = Mobile_data(request)
        self.assertIn(b'exists', response.content)


class CustomErrorHandlerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_404_returns_404_status(self):
        request = self.factory.get('/nonexistent/')
        response = custom_404(request, Exception("Not found"))
        self.assertEqual(response.status_code, 404)

    def test_custom_500_returns_500_status(self):
        request = self.factory.get('/')
        response = custom_500(request)
        self.assertEqual(response.status_code, 500)


class LoginRequiredMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LoginRequiredMiddleware(
            get_response=lambda r: JsonResponse({"ok": True})
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_unauthenticated_user_is_redirected(self):
        from django.contrib.auth.models import AnonymousUser
        request = self.factory.get('/laptop/search/')
        request.user = AnonymousUser()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_passes_through(self):
        request = self.factory.get('/laptop/search/')
        request.user = self.user
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_login_url_is_exempt(self):
        from django.contrib.auth.models import AnonymousUser
        request = self.factory.get('/accounts/login/')
        request.user = AnonymousUser()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)


class ErrorHandlerMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ErrorHandlerMiddleware(get_response=lambda r: None)

    def test_resolver404_returns_404_response(self):
        request = self.factory.get('/login.cgi')
        exc = Resolver404({'tried': [], 'path': 'login.cgi'})
        response = self.middleware.process_exception(request, exc)
        self.assertEqual(response.status_code, 404)

    def test_generic_exception_returns_500_response(self):
        request = self.factory.get('/')
        response = self.middleware.process_exception(request, Exception("unexpected"))
        self.assertEqual(response.status_code, 500)


class LaptopsDataExceptionHandlingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_post_missing_hdd_type_returns_error(self):
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'Dell',
            'inputLapModel': 'Latitude',
            'inputLapRAM': '16',
            'inputLapHDD': '512',
            'inputLapProcessor': 'Intel i7',
            'inputLapSerialNo': 'SN-100',
            'inputLapassetid': 'ASSET-100',
            'inputLapuname': 'newuser',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertIn(b'HDD Type', response.content)

    @patch('assets.views.Laptops_records.objects')
    def test_post_database_error_returns_500(self, mock_objects):
        mock_objects.filter.return_value.exists.side_effect = Exception("DB error")
        request = self.factory.post('/Laptops_data/', {
            'inputLapMake': 'Dell',
            'inputLapModel': 'Latitude',
            'inputLapRAM': '16',
            'inputLapHDDType': 'GB',
            'inputLapHDD': '512',
            'inputLapProcessor': 'Intel i7',
            'inputLapSerialNo': 'SN-100',
            'inputLapassetid': 'ASSET-100',
            'inputLapuname': 'newuser',
        })
        request.user = self.user
        response = Laptops_data(request)
        self.assertEqual(response.status_code, 500)


class MobileDataExceptionHandlingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    @patch('assets.views.Mobile_records.objects')
    def test_post_database_error_returns_500(self, mock_objects):
        mock_objects.filter.return_value.exists.side_effect = Exception("DB error")
        request = self.factory.post('/Mobile_data/', {
            'inputMobMake': 'Samsung',
            'inputMobModel': 'Galaxy S23',
            'inputMobIMIE': '123456789012345',
            'inputMobSerialNo': 'MSN-100',
            'inputMobassetid': 'MOB-100',
            'inputMobuname': 'mobileuser',
        })
        request.user = self.user
        response = Mobile_data(request)
        self.assertEqual(response.status_code, 500)
