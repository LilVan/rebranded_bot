# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    specialty = models.ForeignKey('Specialties', models.DO_NOTHING)
    doctor_last_name = models.TextField()
    doctor_first_name = models.TextField()
    doctor_user_name = models.TextField(default=None, blank=True, null=True)
    doctor_patronymic = models.TextField(blank=True, null=True)
    doctor_fee = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'doctors'


class Measurements(models.Model):
    measurement_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patients', models.DO_NOTHING)
    measurement_date = models.TextField()
    height = models.TextField(blank=True, null=True)  # This field type is a guess.
    weight = models.TextField(blank=True, null=True)  # This field type is a guess.
    body_temperature = models.TextField(blank=True, null=True)  # This field type is a guess.
    systolic_bp = models.IntegerField(blank=True, null=True)
    diastolic_bp = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey(Doctors, models.DO_NOTHING)

    class Meta:
        db_table = 'measurements'


class Nurses(models.Model):
    nurse_id = models.AutoField(primary_key=True)
    nurse_last_name = models.TextField()
    nurse_first_name = models.TextField()
    nurse_patronymic = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'nurses'


class NursesMeasurements(models.Model):
    nurse = models.OneToOneField(Nurses, models.DO_NOTHING, primary_key=True)
    measurement = models.ForeignKey(Measurements, models.DO_NOTHING)

    class Meta:
        db_table = 'nurses_measurements'


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_snils = models.TextField(unique=True)
    patient_last_name = models.TextField()
    patient_first_name = models.TextField()
    patient_patronymic = models.TextField(blank=True, null=True)
    patient_gender = models.TextField()
    patient_date_of_birth = models.TextField()

    class Meta:
        db_table = 'patients'


class Specialties(models.Model):
    specialty_id = models.AutoField(primary_key=True)
    specialty_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'specialties'
