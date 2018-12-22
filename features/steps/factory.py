import os

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from i18nfield.strings import LazyI18nString

from api.engine.models import *

from faker import Faker
fake = Faker()


def create_receipt_photo(reservation, photo=None):
    result = ReceiptPhoto(reservation=reservation)
    result.save()

    return result


def create_reservation(room, user):
    result = Reservation.create(room_characteristics=room, user=user)

    return result


def create_uploaded_file(self, file_name):
    self.expected_file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(self.expected_file_path):
        os.remove(self.expected_file_path)

    photo_file = File(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), file_name), 'rb'))

    result = SimpleUploadedFile(file_name, photo_file.read(),
                                content_type='multipart/form-data')

    return result


def create_currency(symbol, code):
    result = Currency.objects.filter(code=code).first()

    if not result:
        Currency(symbol=symbol, code=code).save()
        result = Currency.objects.filter(symbol=symbol).first()

    return result


def create_bank_account(bank_name, account_number, currency, dormitory):
    result = BankAccount(bank_name=bank_name, account_number=account_number,
                         currency=currency, dormitory=dormitory)

    result.save()
    return result


def create_category(name):
    DormitoryCategory(name=name).save()
    result = DormitoryCategory.objects.filter(name=name).first()

    return result


def create_dorm(name, category, manager=None):
    result = Dormitory(name=name)
    result.category = category

    if manager:
        result.manager = manager
    else:
        manager = User(first_name=fake.name(), username=fake.name())
        manager.is_manager = True
        manager.save()
        result.manager = manager

    result.save()

    return result


def create_integral_choice(integral_filter, number):
    result = IntegralChoice(selected_number=number)
    result.related_filter = integral_filter
    result.save()

    result = IntegralChoice.objects.filter(related_filter__name=integral_filter.name,
                                           selected_number=number).first()

    return result


def create_radio_filter(options, name):
    result = RadioFilter(name=name)
    result.save()

    for option in options:
        option.related_filter = result
        option.save()
        option = RadioOption.objects.filter(name=option.name)

    result = RadioFilter.objects.filter(name=name).first()

    return result


def create_dorm_feature(name):
    result = FeatureFilter(name=name, is_dorm_feature=True)
    result.save()
    result = FeatureFilter.objects.filter(name=name).first()

    return result


def create_room_feature(name):
    result = FeatureFilter(name=name)
    result.save()
    result = FeatureFilter.objects.filter(name=name).first()

    return result


def create_radio_choice(selected_option, radio_filter):
    result = RadioChoice()
    result.selected_option = selected_option
    result.related_filter = radio_filter
    result.save()

    result = RadioChoice.objects.get(pk=result.id)

    return result


def create_room(dorm):
    dollar_currency = create_currency('$', 'USD')

    result = RoomCharacteristics(dormitory=dorm, price_currency=dollar_currency)
    result.save()

    return result


def create_room_with_radio_choices(dorm, choices):
    dollar_currency = create_currency('$', 'USD')

    result = RoomCharacteristics(dormitory=dorm, allowed_quota=5, price_currency=dollar_currency)
    result.save()

    for choice in choices:
        result.radio_choices.add(choice)
    result.save()

    return result


def create_room_with_integral_choices(dorm, choices):
    dollar_currency = create_currency('$', 'USD')

    result = RoomCharacteristics(dormitory=dorm, allowed_quota=5, price_currency=dollar_currency)
    result.save()

    for choice in choices:
        result.integral_choices.add(choice)
    result.save()

    return result


def create_room_with_features(dorm, features):
    dollar_currency = create_currency('$', 'USD')

    result = RoomCharacteristics(dormitory=dorm, allowed_quota=5, price_currency=dollar_currency)
    result.save()

    for feature in features:
        result.features.add(feature)
    result.save()

    return result


def create_room_with_radio_integral_features(dorm, radio_choices, integral_choices, features):
    dollar_currency = create_currency('$', 'USD')

    result = RoomCharacteristics(dormitory=dorm, allowed_quota=5, price_currency=dollar_currency)
    result.save()

    for choice in radio_choices:
        result.radio_choices.add(choice)
    result.save()

    for choice in integral_choices:
        result.integral_choices.add(choice)
    result.save()

    for feature in features:
        result.features.add(feature)
    result.save()

    return result


def create_manager(self, name):
    result = User(first_name=name, username=name)
    result.is_manager = True

    result.save()

    return result


def create_student(self, name):
    result = User(first_name=name, username=name)

    result.save()

    return result


def create_alfam_dovec_with_4_rooms(self):

    self.category_public = create_category('public')
    self.category_private = create_category('private')

    self.alfam = create_dorm('Alfam', self.category_public)
    self.dovec = create_dorm('Dovec', self.category_private)

    self.swimming_pool = create_dorm_feature('Swimming pool')
    self.free_wifi = create_dorm_feature('Free WiFi')

    self.alfam.features.add(self.swimming_pool)
    self.alfam.save()
    self.dovec.features.add(self.free_wifi)
    self.dovec.save()

    self.luxury_shower = create_room_feature('Luxury shower')
    self.air_conditioner = create_room_feature('Air Conditioner')

    self.price_filter = IntegralFilter(name='Price')
    self.price_filter.save()
    self.price_1000 = create_integral_choice(self.price_filter, 1000)
    self.price_1200 = create_integral_choice(self.price_filter, 1200)
    self.price_1700 = create_integral_choice(self.price_filter, 1700)
    self.price_2000 = create_integral_choice(self.price_filter, 2000)

    self.people_allowed_number_filter = IntegralFilter(name='People Allowed Number')
    self.people_allowed_number_filter.save()
    self.one_person = create_integral_choice(self.people_allowed_number_filter, 1)
    self.two_persons = create_integral_choice(self.people_allowed_number_filter, 2)
    self.three_persons = create_integral_choice(self.people_allowed_number_filter, 3)
    self.four_persons = create_integral_choice(self.people_allowed_number_filter, 4)

    self.bathrooms = IntegralFilter(name='bathroom')
    self.bathrooms.save()
    self.bathrooms1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms2 = create_integral_choice(self.bathrooms, 2)

    self.meal_options = [RadioOption(name='Breakfast'),
                         RadioOption(name='Dinner'),
                         RadioOption(name='Both')]
    self.meals = create_radio_filter(self.meal_options, 'Meals')
    self.meals_choice_breakfast = create_radio_choice(self.meal_options[0], self.meals)
    self.meals_choice_dinner = create_radio_choice(self.meal_options[1], self.meals)
    self.meals_choice_both = create_radio_choice(self.meal_options[2], self.meals)

    self.room_type_options = [RadioOption(name='Single'),
                              RadioOption(name='Double'),
                              RadioOption(name='Studio')]
    self.room_types = create_radio_filter(self.room_type_options, 'Room Type')
    self.room_type_single_choice = create_radio_choice(self.room_type_options[0], self.room_types)
    self.room_type_double_choice = create_radio_choice(self.room_type_options[1], self.room_types)
    self.room_type_studio_choice = create_radio_choice(self.room_type_options[2], self.room_types)

    self.options_duration = [RadioOption(name='Spring'), RadioOption(name='Winter'),
                             RadioOption(name='Summer'), RadioOption(name='Full year')]
    self.duration = create_radio_filter(self.options_duration, 'Duration')
    self.duration_choice_spring = create_radio_choice(
        self.options_duration[0], self.duration)
    self.duration_choice_winter = create_radio_choice(
        self.options_duration[1], self.duration)
    self.duration_choice_summer = create_radio_choice(
        self.options_duration[2], self.duration)
    self.duration_choice_full = create_radio_choice(
        self.options_duration[3], self.duration)

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.duration_choice_spring, self.room_type_studio_choice],
        [self.price_1000, self.one_person],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.meals_choice_breakfast, self.duration_choice_spring, self.room_type_single_choice],
        [self.price_1200, self.bathrooms1, self.one_person],
        [self.air_conditioner, ])

    self.room3 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_breakfast, self.duration_choice_spring, self.room_type_double_choice],
        [self.price_1700, self.two_persons],
        [self.luxury_shower, ])

    self.room4 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_both, self.duration_choice_full, self.room_type_double_choice],
        [self.price_2000, self.bathrooms2, self.two_persons],
        [self.luxury_shower, self.air_conditioner])


def fill_dorm_data(dorm, *args, **kwargs):
    for attr, value in kwargs.items():
        setattr(dorm, attr, value)

    dorm.save()


def create_alfam_dovec_with_4_rooms_localized_en_tr(self):
    alfam_about_en = """In an ideal world this website wouldn’t exist, a client would acknowledge the importance of having web copy before the design starts. Needless to say it’s very important, content is king and people are beginning to understand that.


    We believe that staying in a dormitory where all types of technological, cultural and sportive facilities are offered under campus safety, will be a best start for your academic life."""

    alfam_about_tr = """İdeal bir dünyada, bu web sitesi mevcut değildi, bir müşteri tasarımın başlamasından önce web kopyasının önemini kabul ederdi. Çok önemli olduğunu söylemeye gerek yok, içerik kraldır ve insanlar bunu anlamaya başlıyor.


    Kampüs güvenliği altında her türlü teknolojik, kültürel ve sportif tesislerin sunulduğu bir yurtta kalmanın akademik hayatınız için en iyi başlangıç olacağına inanıyoruz."""

    dovec_about_en = """We believe that staying in a dormitory where all types of technological, cultural and sportive facilities are offered under campus safety, will be a best start for your academic life. 

    In an ideal world this website wouldn’t exist, a client would acknowledge the importance of having web copy before the design starts. Needless to say it’s very important, content is king and people are beginning to understand that."""

    dovec_about_tr = """Kampüs güvenliği altında her türlü teknolojik, kültürel ve sportif tesislerin sunulduğu bir yurtta kalmanın akademik hayatınız için en iyi başlangıç olacağına inanıyoruz.

    İdeal bir dünyada, bu web sitesi mevcut değildi, bir müşteri tasarımın başlamasından önce web kopyasının önemini kabul ederdi. Çok önemli olduğunu söylemeye gerek yok, içerik kraldır ve insanlar bunu anlamaya başlıyor."""

    self.category_public = create_category(LazyI18nString({'tr': 'Genel', 'en': 'Public'}))
    self.category_private = create_category(LazyI18nString({'tr': 'Özel', 'en': 'Private'}))

    self.alfam = create_dorm('Alfam', self.category_public)
    self.dovec = create_dorm('Dovec', self.category_private)

    self.swimming_pool = create_dorm_feature(
        LazyI18nString({'tr': 'Yüzme Havuzu', 'en': 'Swimming Pool'}))
    self.free_wifi = create_dorm_feature(LazyI18nString(
        {'tr': 'Bedava Internet', 'en': 'Free WiFi'}))

    self.alfam.features.add(self.swimming_pool)
    fill_dorm_data(self.alfam,
                   about=LazyI18nString({'tr': alfam_about_tr, 'en': alfam_about_en}),
                   geo_longitude='35.1501', geo_latitude='33.90111',
                   address='Next to Computer Department',
                   contact_name='Mohammed Alhakem', contact_email='Alhakeem@gmail.com',
                   contact_number='+905338524788', contact_fax='+9021555455')
    self.alfam.save()

    self.dovec.features.add(self.free_wifi)
    fill_dorm_data(self.dovec,
                   about=LazyI18nString({'tr': dovec_about_tr, 'en': dovec_about_en}),
                   geo_longitude='35.2020', geo_latitude='33.90900',
                   address='Next to Electric Faculty',
                   contact_name='Yaser Alnajjar', contact_email='Alnajjar@gmail.com',
                   contact_number='+905338882626', contact_fax='+90123456')
    self.dovec.save()

    self.luxury_shower = create_room_feature(
        LazyI18nString({'tr': 'Lüks Duş', 'en': 'Luxury shower'}))
    self.air_conditioner = create_room_feature(
        LazyI18nString({'tr': 'Klima', 'en': 'Air Conditioner'}))

    self.price_filter = IntegralFilter(name=LazyI18nString({'tr': 'Fiyat', 'en': 'Price'}))
    self.price_filter.save()
    self.price_1000 = create_integral_choice(self.price_filter, 1000)
    self.price_1200 = create_integral_choice(self.price_filter, 1200)
    self.price_1700 = create_integral_choice(self.price_filter, 1700)
    self.price_2000 = create_integral_choice(self.price_filter, 2000)

    self.people_allowed_number_filter = IntegralFilter(name=LazyI18nString(
        {'tr': 'Kişi İzin Numarası', 'en': 'People Allowed Number'}))
    self.people_allowed_number_filter.save()
    self.one_person = create_integral_choice(self.people_allowed_number_filter, 1)
    self.two_persons = create_integral_choice(self.people_allowed_number_filter, 2)
    self.three_persons = create_integral_choice(self.people_allowed_number_filter, 3)
    self.four_persons = create_integral_choice(self.people_allowed_number_filter, 4)

    self.bathrooms = IntegralFilter(name=LazyI18nString({'tr': 'Banyo', 'en': 'Bathroom'}))
    self.bathrooms.save()
    self.bathrooms1 = create_integral_choice(self.bathrooms, 1)
    self.bathrooms2 = create_integral_choice(self.bathrooms, 2)

    self.meal_options = [RadioOption(name=LazyI18nString({'tr': 'Kahvaltı', 'en': 'Breakfast'})),
                         RadioOption(name=LazyI18nString({'tr': 'Akşam Yemegi', 'en': 'Dinner'})),
                         RadioOption(name=LazyI18nString({'tr': 'Her Ikisi de', 'en': 'Both'}))]
    self.meals = create_radio_filter(
        self.meal_options, LazyI18nString({'tr': 'Yemekler', 'en': 'Meals'}))
    self.meals_choice_breakfast = create_radio_choice(self.meal_options[0], self.meals)
    self.meals_choice_dinner = create_radio_choice(self.meal_options[1], self.meals)
    self.meals_choice_both = create_radio_choice(self.meal_options[2], self.meals)

    self.room_type_options = [RadioOption(name=LazyI18nString({'tr': 'Tek ', 'en': 'Single'})),
                              RadioOption(name=LazyI18nString(
                                  {'tr': 'Çift Kişilik', 'en': 'Double'})),
                              RadioOption(name=LazyI18nString({'tr': 'Stüdyo', 'en': 'Studio'}))]
    self.room_types = create_radio_filter(self.room_type_options, LazyI18nString({
                                          'tr': 'Oda Tipi ', 'en': 'Room Type'}))
    self.room_type_single_choice = create_radio_choice(self.room_type_options[0], self.room_types)
    self.room_type_double_choice = create_radio_choice(self.room_type_options[1], self.room_types)
    self.room_type_studio_choice = create_radio_choice(self.room_type_options[2], self.room_types)

    self.options_duration = [RadioOption(name=LazyI18nString({'tr': 'Bahar', 'en': 'Spring'})),
                             RadioOption(name=LazyI18nString({'tr': 'Kış', 'en': 'Winter'})),
                             RadioOption(name=LazyI18nString({'tr': 'Yaz', 'en': 'Summer'})),
                             RadioOption(name=LazyI18nString({'tr': 'Tüm Yıl', 'en': 'Full Year'}))]
    self.duration = create_radio_filter(
        self.options_duration, LazyI18nString({'tr': 'Süre', 'en': 'Duration'}))
    self.duration_choice_spring = create_radio_choice(
        self.options_duration[0], self.duration)
    self.duration_choice_winter = create_radio_choice(
        self.options_duration[1], self.duration)
    self.duration_choice_summer = create_radio_choice(
        self.options_duration[2], self.duration)
    self.duration_choice_full = create_radio_choice(
        self.options_duration[3], self.duration)

    self.room1 = create_room_with_radio_integral_features(
        self.alfam,
        [self.duration_choice_spring, self.room_type_studio_choice],
        [self.price_1000, self.one_person],
        [])

    self.room2 = create_room_with_radio_integral_features(
        self.alfam,
        [self.meals_choice_breakfast, self.duration_choice_spring, self.room_type_single_choice],
        [self.price_1200, self.bathrooms1, self.one_person],
        [self.air_conditioner, ])

    self.room3 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_breakfast, self.duration_choice_spring, self.room_type_double_choice],
        [self.price_1700, self.two_persons],
        [self.luxury_shower, ])

    self.room4 = create_room_with_radio_integral_features(
        self.dovec,
        [self.meals_choice_both, self.duration_choice_full, self.room_type_double_choice],
        [self.price_2000, self.bathrooms2, self.two_persons],
        [self.luxury_shower, self.air_conditioner])
