# Generated by Django 3.2.3 on 2021-07-01 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210616_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printhead',
            name='password',
        ),
        migrations.AddField(
            model_name='printtype',
            name='method',
            field=models.CharField(default='print_contest_pdf', max_length=100, verbose_name='メソッド'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.unit', verbose_name='単元'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.grade', verbose_name='学年'),
        ),
    ]
