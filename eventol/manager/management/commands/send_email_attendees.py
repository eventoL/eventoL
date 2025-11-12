# mailing/management/commands/send_email_attendees.py
import os
import time
from itertools import islice
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from manager.models import Attendee

# Constantes para la estrategia de envío
BATCH_SIZE = 10
DELAY_SECONDS = 3


class Command(BaseCommand):
    help = 'Envía un correo electrónico multipart en lotes con reintentos recursivos en caso de fallo.'

    # ... (El método add_arguments se mantiene igual) ...
    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, required=True, help='Asunto del correo electrónico.')
        parser.add_argument(
            '--recipients', type=str, required=False, help='Lista de destinatarios separados por comas.'
        )
        parser.add_argument(
            '--filepath-text', type=str, required=True, help='Ruta al archivo con contenido de texto plano.'
        )
        parser.add_argument('--filepath-html', type=str, required=True, help='Ruta al archivo con contenido HTML.')
        parser.add_argument(
            '--event-id', type=int, required=False, help='ID del evento para enviar a los asistentes registrados.'
        )

    def _get_file_content(self, filepath, content_type):
        """Función auxiliar para leer el contenido de los archivos."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise CommandError(f'Error: Archivo {content_type} no encontrado en: {filepath}')
        except Exception as e:
            raise CommandError(f'Error al leer el archivo {content_type}: {e}')

    # 🚀 Función Recursiva de Envío y Reintento
    def _send_batch(self, recipients, subject, text_content, html_content, from_email):
        """
        Intenta enviar el correo a la lista de destinatarios.
        Si falla, divide la lista y reintenta recursivamente.
        """
        if not recipients:
            return  # Lista vacía, no hace nada

        if len(recipients) == 1:
            self.stdout.write(
                self.style.WARNING(
                    f'Aislado: Fallo al enviar el correo a la única dirección problemática: {recipients[0]}'
                )
            )
            return

        try:
            # 1. Crear el mensaje con todos en BCC
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=[], bcc=recipients)
            msg.attach_alternative(html_content, 'text/html')

            # 2. Intentar el envío
            self.stdout.write(self.style.NOTICE(f'  -> Intentando enviar a lote de {len(recipients)}...'))
            msg.send()
            self.stdout.write(self.style.SUCCESS(f'  -> Lote de {len(recipients)} enviado correctamente.'))

        except Exception as e:
            # 3. Lógica de Reintento Recursivo si el envío falla
            self.stdout.write(
                self.style.ERROR(
                    f'\n[ERROR EN BATCH] Falla al enviar lote de {len(recipients)}. Dividiendo y reintentando...'
                )
            )
            self.stdout.write(f'  Detalle de la falla: {e}')

            # Dividir la lista en dos mitades
            mid_point = len(recipients) // 2
            list_a = recipients[:mid_point]
            list_b = recipients[mid_point:]

            # Reintento recursivo en la primera mitad
            self.stdout.write(self.style.WARNING(f'  Reintentando Mitad A ({len(list_a)})...'))
            self._send_batch(list_a, subject, text_content, html_content, from_email)

            # Reintento recursivo en la segunda mitad
            self.stdout.write(self.style.WARNING(f'  Reintentando Mitad B ({len(list_b)})...'))
            self._send_batch(list_b, subject, text_content, html_content, from_email)

    # 🧩 Método principal
    def handle(self, *args, **options):
        # 1. Preparación de datos
        subject = options['subject']
        event_id = options.get('event_id')

        if event_id:
            full_recipient_list = [attendee.email for attendee in Attendee.objects.filter(event_id=event_id)]
        elif options.get('recipients'):
            # Usamos la lógica robusta para limpiar la lista de destinatarios
            recipient_list_str = options['recipients']
            full_recipient_list = [r.strip() for r in recipient_list_str.split(',') if r.strip()]
        else:
            raise CommandError('Debe proporcionar --event-id o --recipients.')

        filepath_text = options['filepath_text']
        filepath_html = options['filepath_html']

        text_content = self._get_file_content(filepath_text, 'texto plano')
        html_content = self._get_file_content(filepath_html, 'HTML')

        from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'tu.email@ejemplo.com'

        total_recipients = len(full_recipient_list)
        self.stdout.write(
            self.style.SUCCESS(f'Iniciando envío de {total_recipients} correos en lotes de {BATCH_SIZE}.')
        )

        # 2. Chunking (división en lotes) e invocación

        # Iterador para dividir la lista completa en lotes de 10
        recipient_chunks = [full_recipient_list[i : i + BATCH_SIZE] for i in range(0, total_recipients, BATCH_SIZE)]

        for i, chunk in enumerate(recipient_chunks):
            chunk_start = i * BATCH_SIZE + 1
            chunk_end = chunk_start + len(chunk) - 1

            self.stdout.write(f'\n--- Procesando Lote {i + 1} ({chunk_start} a {chunk_end} de {total_recipients}) ---')

            # Llamada al proceso recursivo de envío y reintento
            self._send_batch(chunk, subject, text_content, html_content, from_email)

            # 3. Espera entre lotes
            if i < len(recipient_chunks) - 1:
                self.stdout.write(f'Esperando {DELAY_SECONDS} segundos antes del siguiente lote...')
                time.sleep(DELAY_SECONDS)

        self.stdout.write(
            self.style.SUCCESS(
                '\n¡Proceso de envío completado! Revisa los logs para ver los emails problemáticos aislados.'
            )
        )
