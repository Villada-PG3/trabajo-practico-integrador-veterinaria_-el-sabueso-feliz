from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sabueso_feliz', '0002_alter_calendariovacuna_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estudiantes',
            options={'ordering': ['empleado__apellido', 'empleado__nombre'], 'verbose_name': 'Estudiante', 'verbose_name_plural': 'Estudiantes'},
        ),
        migrations.AlterModelOptions(
            name='veterinario',
            options={'ordering': ['empleado__apellido', 'empleado__nombre'], 'verbose_name': 'Veterinario', 'verbose_name_plural': 'Veterinarios'},
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name='veterinario',
                    name='empleado_ptr',
                ),
                migrations.AddField(
                    model_name='veterinario',
                    name='empleado',
                    field=models.OneToOneField(
                        db_column='empleado_ptr_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='veterinario',
                        serialize=False,
                        to='sabueso_feliz.empleado',
                        verbose_name='Empleado asignado',
                    ),
                ),
                migrations.RemoveField(
                    model_name='estudiantes',
                    name='empleado_ptr',
                ),
                migrations.AddField(
                    model_name='estudiantes',
                    name='empleado',
                    field=models.OneToOneField(
                        db_column='empleado_ptr_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='estudiantes',
                        serialize=False,
                        to='sabueso_feliz.empleado',
                        verbose_name='Empleado asignado',
                    ),
                ),
            ],
        ),
    ]
