# invoices/utils.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Заголовок
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"СЧЁТ №{invoice.id}")

    # Реквизиты компании (можно настроить в settings)
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 80, "Freelancer CRM")
    p.drawString(50, height - 95, "ИНН: 1234567890")
    p.drawString(50, height - 110, "Р/с: 40802810123450000123")

    # Данные клиента
    p.drawString(50, height - 140, f"Клиент: {invoice.project.client.name}")
    p.drawString(50, height - 155, f"Email: {invoice.project.client.email}")

    # Проект
    p.drawString(50, height - 185, f"Проект: {invoice.project.name}")
    p.drawString(50, height - 200, f"Сумма: {invoice.amount} руб.")
    p.drawString(50, height - 215, f"Дата оплаты: {invoice.due_date.strftime('%d.%m.%Y')}")
    p.drawString(50, height - 230, f"Статус: {invoice.get_status_display()}")

    # Подпись
    p.drawString(50, 100, "Счёт выставлен автоматически. Подпись не требуется.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer