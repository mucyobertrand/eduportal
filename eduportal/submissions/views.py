import subprocess
from pathlib import Path
from django.shortcuts import render, redirect
from django.conf import settings
from .models import StudentSubmission

def dashboard(request):
    """READ: Fetches records and metric counters for the interface."""
    items = StudentSubmission.objects.all().order_by('-uploaded_at')
    
    # Calculate values for the dashboard alerts bar
    unsorted_count = StudentSubmission.objects.filter(status='UNSORTED').count()
    sorted_count = StudentSubmission.objects.filter(status='SORTED').count()
    
    context = {
        'submissions': items,
        'unsorted_count': unsorted_count,
        'sorted_count': sorted_count,
    }
    return render(request, 'submissions/dashboard.html', context)

def upload_file(request):
    """CREATE: Safely logs inbound files onto the local disk."""
    if request.method == "POST" and request.FILES.get('student_file'):
        student = request.POST.get('student_name')
        file_obj = request.FILES['student_file']

        # Ensure raw incoming target area path exists
        inbox_dir = Path(settings.MEDIA_ROOT) / "raw_inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        saved_path = inbox_dir / file_obj.name
        with open(saved_path, 'wb+') as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)

        # Build index mapping card inside the database
        StudentSubmission.objects.create(
            student_name=student,
            file_name=file_obj.name,
            current_file_path=str(saved_path),
            status='UNSORTED'
        )
        return redirect('dashboard')
    
    return render(request, 'submissions/upload.html')

def execute_sorting_pipeline(request):
    """AUTOMATION PIPELINE: Runs your custom package over targeted paths."""
    if request.method == "POST":
        target_path = Path(settings.MEDIA_ROOT) / "raw_inbox"
        
        try:
            # Executes your exact global CLI pip package command
            subprocess.run(
                ["smart-organize", str(target_path)],
                check=True
            )
            
            # Re-index files shifted by the package engine
            for entry in StudentSubmission.objects.filter(status='UNSORTED'):
                orig_path = Path(entry.current_file_path)
                ext = orig_path.suffix.lower()
                
                # Align categories to mirror your package's folder logic
                category = "Others"
                if ext in ['.pdf', '.docx', '.txt']: category = "Documents"
                elif ext in ['.png', '.jpg', '.jpeg']: category = "Images"
                elif ext in ['.zip', '.tar', '.gz']: category = "Archives"
                
                resolved_path = target_path / category / entry.file_name
                
                if resolved_path.exists():
                    entry.current_file_path = str(resolved_path)
                    entry.status = 'SORTED'
                    entry.save()

        except subprocess.CalledProcessError as e:
            print(f"Subprocess wrapper failed execution: {e}")
            
    return redirect('dashboard')
