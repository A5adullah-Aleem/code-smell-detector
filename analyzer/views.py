from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from .code_analysis import  analyze_folder, parse_code, AntiPatternVisitor


def analyze_code(request):
    if request.method == "POST" and request.FILES.getlist('code_files'):
        files = request.FILES.getlist('code_files')
        report = []

        # Save and process each uploaded file
        for uploaded_file in files:
            fs = FileSystemStorage(location='uploads/')
            file_path = fs.save(uploaded_file.name, uploaded_file)
            full_file_path = os.path.join(fs.location, file_path)
            tree = parse_code(full_file_path)
            visitor = AntiPatternVisitor()
            visitor.visit(tree)
            for item in visitor.report:
                item["file"] = full_file_path
                report.append(item)

        return render(request, 'report.html', {'report': report})

    return render(request, 'upload.html')







"""from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from .code_analysis import analyze_folder

def analyze_code(request):
    if request.method == "POST" and request.FILES.get('code_folder'):
        uploaded_folder = request.FILES['code_folder']
        fs = FileSystemStorage(location='uploads/')
        folder_path = fs.save(uploaded_folder.name, uploaded_folder)
        
        full_folder_path = os.path.join(fs.location, folder_path)
        report = analyze_folder(full_folder_path)
        
        print(f"Full folder path: {full_folder_path}")
        print(f"Report generated: {report}")

        
        return render(request, 'report.html', {'report': report})

    return render(request, 'upload.html')"""
