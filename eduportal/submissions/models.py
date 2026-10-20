from django.db import models

class StudentSubmission(models.Model):
    STATUS_CHOICES = [
        ('UNSORTED', 'Unsorted (In Dropzone)'),
        ('SORTED', 'Sorted & Categorized'),
    ]

    student_name = models.CharField(max_length=150)
    file_name = models.CharField(max_length=255)
    current_file_path = models.CharField(max_length=512)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNSORTED')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.file_name}"
