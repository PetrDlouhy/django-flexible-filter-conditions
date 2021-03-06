# Generated by Django 2.2.9 on 2020-01-14 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('and', 'and'), ('or', 'or'), ('nor', 'nor')], max_length=30, verbose_name='Operation')),
                ('conds', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conds_rel', to='flexible_filter_conditions.Condition', verbose_name='Conditions')),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
            },
        ),
        migrations.CreateModel(
            name='NamedCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name of condition')),
                ('as_filter', models.BooleanField(default=False, help_text='Determines whether this condition is available as a filterin the table of Users', verbose_name='Display as filter?')),
                ('on_dashboard', models.BooleanField(default=False, help_text='Determines whether this condition is available on dashboard', verbose_name='Display on dashboard?')),
            ],
            options={
                'verbose_name': 'Condition',
                'ordering': ('name',),
                'verbose_name_plural': 'Conditions',
            },
        ),
        migrations.CreateModel(
            name='TerminalCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(blank=True, choices=[('action', "Action: CharField ('daily', 'new-user', 'new-payment')"), ('TestModel', [('TestModel.id', 'id: AutoField '), ('TestModel.test_field', 'test_field: CharField ')]), ('User', [('User.id', 'id: AutoField '), ('User.password', 'password: CharField '), ('User.last_login', 'last_login: DateTimeField '), ('User.is_superuser', 'is_superuser: BooleanField '), ('User.username', 'username: CharField '), ('User.first_name', 'first_name: CharField '), ('User.last_name', 'last_name: CharField '), ('User.email', 'email: CharField '), ('User.is_staff', 'is_staff: BooleanField '), ('User.is_active', 'is_active: BooleanField '), ('User.date_joined', 'date_joined: DateTimeField ')])], help_text='Value or variable on left-hand side', max_length=50, null=True, verbose_name='Variable')),
                ('operation', models.CharField(choices=[('=', '='), ('!=', '≠'), ('>', '>'), ('<', '<'), ('>=', '≤'), ('<=', '≤'), ('containts', 'contains'), ('icontaints', 'contains (case insensitive)')], max_length=30, verbose_name='Operation')),
                ('value', models.CharField(blank=True, help_text='Value or variable on right-hand side. <br/>\naction: daily, new-user<br/>\nDateField: month_ago, one_day, one_week, two_weeks, one_month<br/>\nBooleanField: True, False', max_length=50, null=True, verbose_name='Value')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flexible_filter_conditions.Condition')),
            ],
            options={
                'verbose_name': 'Terminal condition',
                'verbose_name_plural': 'Terminal conditions',
            },
        ),
        migrations.AddField(
            model_name='condition',
            name='named_condition',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condition', to='flexible_filter_conditions.NamedCondition'),
        ),
        migrations.AddConstraint(
            model_name='condition',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('named_condition__isnull', False), ('conds__isnull', False), _connector='OR'), models.Q(('named_condition__isnull', True), ('conds__isnull', True), _connector='OR')), name='conds_xor_named_condition_is_null'),
        ),
    ]
