# Generated by Django 2.2.24 on 2021-11-26 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models
import umnoc.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_overviews', '0024_overview_adds_has_highlights'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('course_overview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='umnoc_courses', to='course_overviews.CourseOverview')),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('uuid', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
                ('published_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', when={'published'})),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('uuid', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
                ('published_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', when={'published'})),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
                ('published_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', when={'published'})),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('uuid', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('published_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', when={'published'})),
                ('title', models.CharField(default='', max_length=1024, verbose_name='Наименование')),
                ('short_name', models.CharField(default='', max_length=64, unique=True, verbose_name='Аббревиатура')),
                ('slug', models.CharField(default='', max_length=64, unique=True, verbose_name='Человеко-понятный уникальный идентификатор')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, help_text='Please add only .PNG files for logo images. This logo will be used on Program logo.', max_length=255, null=True, upload_to='program_logos')),
                ('image_background', models.ImageField(blank=True, help_text='Please add only .PNG files for background images. This image will be used on Program background image.', null=True, upload_to='program_background')),
                ('active', models.BooleanField(default=True)),
                ('enrollment_allowed', models.CharField(choices=[('Недоступна', 'Недоступна'), ('Доступна', 'Доступна'), ('По расписанию', 'По расписанию')], default='2', max_length=1, verbose_name='Доступность записи')),
                ('id_unit_program', models.CharField(blank=True, max_length=64, null=True, verbose_name='Программа ID')),
                ('edu_start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала программы')),
                ('edu_end_date', models.DateField(blank=True, null=True, verbose_name='Дата завершения программы')),
                ('number_of_hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество часов')),
                ('issued_document_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Выдаваемый Документ')),
                ('direction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='umnoc.Direction')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='programs', to='umnoc.Organization')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='realized_programs', to='umnoc.Project')),
            ],
            options={
                'verbose_name': 'образовательная программа',
                'verbose_name_plural': 'образовательные программы',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('second_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('sex', models.CharField(choices=[('m', 'мужской'), ('f', 'женский')], max_length=1, verbose_name='Пол')),
                ('birth_date', models.CharField(max_length=16, verbose_name='Дата рождения')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
                ('city', models.CharField(max_length=256, null=True, verbose_name='Город')),
                ('job', models.CharField(max_length=2048, null=True, verbose_name='Место работы')),
                ('position', models.CharField(max_length=2048, null=True, verbose_name='Должность')),
                ('address_register', models.TextField(blank=True, null=True, verbose_name='Адрес регистрации')),
                ('claim_scan', models.FileField(blank=True, null=True, upload_to=umnoc.utils.generate_new_filename, verbose_name='Скан заявления на зачисление в программу ')),
                ('series', models.CharField(max_length=8, null=True, verbose_name='Серия')),
                ('number', models.CharField(max_length=8, null=True, verbose_name='Номер')),
                ('issued_by', models.TextField(null=True, verbose_name='Кем выдан')),
                ('unit_code', models.CharField(max_length=16, null=True, verbose_name='Код подразделения')),
                ('issue_date', models.CharField(max_length=16, null=True, verbose_name='Дата выдачи')),
                ('education_level', models.CharField(choices=[('M', 'Среднее профессиональное'), ('H', 'Высшее')], max_length=1, verbose_name='Уровень базового образования')),
                ('series_diploma', models.CharField(max_length=255, null=True, verbose_name='Серия документа об образовании')),
                ('number_diploma', models.CharField(max_length=255, null=True, verbose_name='Номер документа об образовании')),
                ('edu_organization', models.CharField(blank=True, max_length=355, null=True, verbose_name='Образовательное учреждение')),
                ('specialty', models.CharField(blank=True, max_length=355, null=True, verbose_name='Специальность (направление подготовки)')),
                ('year_of_ending', models.CharField(blank=True, max_length=16, null=True, verbose_name='Год окончания')),
                ('all_valid', models.BooleanField(default=False, verbose_name='Данные в доках слушателя совпадают и корректны')),
                ('doc_forwarding', models.FileField(blank=True, null=True, upload_to=umnoc.utils.generate_new_filename, verbose_name='Скан заявление о пересылке удостоверения слушателя почтой России')),
                ('leader_id', models.CharField(blank=True, max_length=355, null=True, verbose_name='Leader ID')),
                ('SNILS', models.CharField(blank=True, max_length=355, null=True, verbose_name='Номер СНИЛС')),
                ('add_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта для связи')),
                ('birth_place', models.CharField(blank=True, max_length=355, null=True, verbose_name='Место рождения')),
                ('job_address', models.CharField(blank=True, max_length=355, null=True, verbose_name='Адрес работы')),
                ('manager', models.CharField(blank=True, max_length=355, null=True, verbose_name='Ответственный')),
                ('mail_index', models.CharField(blank=True, max_length=255, null=True, verbose_name='Почтовый индекс')),
                ('country', models.CharField(blank=True, default='Россия', max_length=255, null=True, verbose_name='Страна')),
                ('address_living', models.TextField(blank=True, max_length=255, null=True, verbose_name='Адрес проживания')),
                ('terms', models.BooleanField(verbose_name='Я принимаю условия использования и соглашаюсь с политикой конфиденциальности')),
                ('prefered_org', models.CharField(blank=True, max_length=255, null=True, verbose_name='Организация')),
                ('admin_number', models.CharField(blank=True, max_length=355, null=True, verbose_name='Номер согласия')),
                ('admin_diagnostics', models.BooleanField(default=False, verbose_name='Диагностики пройдены')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'анкета для зачисления',
                'verbose_name_plural': 'анкеты для зачисления',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProgramEnrollment',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('external_user_key', models.CharField(db_index=True, max_length=255, null=True)),
                ('program_uuid', models.UUIDField(db_index=True)),
                ('project_uuid', models.UUIDField(db_index=True)),
                ('status', models.CharField(choices=[('enrolled', 'enrolled'), ('pending', 'pending'), ('suspended', 'suspended'), ('canceled', 'canceled'), ('ended', 'ended')], max_length=9)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical program enrollment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ProgramEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('external_user_key', models.CharField(db_index=True, max_length=255, null=True)),
                ('program_uuid', models.UUIDField(db_index=True)),
                ('project_uuid', models.UUIDField(db_index=True)),
                ('status', models.CharField(choices=[('enrolled', 'enrolled'), ('pending', 'pending'), ('suspended', 'suspended'), ('canceled', 'canceled'), ('ended', 'ended')], max_length=9)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='umnoc_programs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'program_uuid', 'project_uuid'), ('external_user_key', 'program_uuid', 'project_uuid')},
            },
        ),
        migrations.CreateModel(
            name='ProgramCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='umnoc.Course')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='umnoc.Program')),
            ],
            options={
                'unique_together': {('course', 'program')},
            },
        ),
        migrations.CreateModel(
            name='OrganizationCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='umnoc.Course')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='umnoc.Program')),
            ],
            options={
                'unique_together': {('course', 'organization')},
            },
        ),
    ]