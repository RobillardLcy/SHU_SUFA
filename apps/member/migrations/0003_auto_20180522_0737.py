# Generated by Django 2.0.4 on 2018-05-22 07:37

from django.db import migrations


def positions(apps, schema_editor):
    Position = apps.get_model("member", "Position")
    db_alias = schema_editor.connection.alias
    Position.objects.using(db_alias).bulk_create([
        Position(name='指导老师', remind='', department_id=1, appointment_id=1),
        Position(name='主席', remind='', department_id=2, appointment_id=2),
        Position(name='副主席', remind='', department_id=2, appointment_id=3),
        Position(name='事务部部长', remind='', department_id=3, appointment_id=4),
        Position(name='事务部副部长', remind='', department_id=3, appointment_id=5),
        Position(name='事务部成员', remind='', department_id=3, appointment_id=17),
        Position(name='外联部部长', remind='', department_id=4, appointment_id=4),
        Position(name='外联部副部长', remind='', department_id=4, appointment_id=6),
        Position(name='外联部成员', remind='', department_id=4, appointment_id=17),
        Position(name='宣传部部长', remind='', department_id=5, appointment_id=4),
        Position(name='宣传部副部长', remind='', department_id=5, appointment_id=7),
        Position(name='宣传部成员', remind='', department_id=5, appointment_id=17),
        Position(name='财务部部长', remind='', department_id=6, appointment_id=4),
        Position(name='财务部副部长', remind='', department_id=6, appointment_id=8),
        Position(name='财务部成员', remind='', department_id=6, appointment_id=17),
        Position(name='技术部部长', remind='', department_id=7, appointment_id=4),
        Position(name='技术部副部长', remind='', department_id=7, appointment_id=9),
        Position(name='技术部成员', remind='', department_id=7, appointment_id=17),
        Position(name='裁判协会会长', remind='', department_id=8, appointment_id=4),
        Position(name='裁判协会副会长', remind='', department_id=8, appointment_id=10),
        Position(name='裁判协会成员', remind='', department_id=8, appointment_id=17),
        Position(name='男足队长', remind='', department_id=9, appointment_id=11),
        Position(name='男足队员', remind='', department_id=9, appointment_id=18),
        Position(name='男足经理', remind='', department_id=9, appointment_id=13),
        Position(name='女足队长', remind='', department_id=9, appointment_id=12),
        Position(name='女足队员', remind='', department_id=9, appointment_id=19),
        Position(name='女足经理', remind='', department_id=9, appointment_id=14),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20180424_0818'),
    ]

    operations = [
        migrations.RunPython(positions),
    ]
