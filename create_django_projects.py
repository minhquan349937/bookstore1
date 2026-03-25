#!/usr/bin/env python
"""
Script tạo cấu trúc Django projects cho Bookstore Microservices
"""
import os
import sys
import subprocess
import shutil

BASE_DIR = r"c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\bookstore_microservices"
SERVICES = ["api_gateway", "staff_service", "customer_service", "book_service", "order_service", "cart_service"]

def run_command(cmd, cwd):
    """Chạy lệnh shell"""
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi: {e.stderr.decode() if e.stderr else e}")
        return False

def create_django_project(service_name):
    """Tạo Django project cho một service"""
    service_path = os.path.join(BASE_DIR, service_name)
    
    print(f"\n{'='*60}")
    print(f"⏳ Khởi tạo: {service_name}")
    print(f"{'='*60}")
    
    # Xóa manage.py và api cũ nếu tồn tại
    files_to_remove = ["manage.py", "api", "db.sqlite3"]
    
    # Tìm và xóa tất cả các thư mục config cũ
    for item in os.listdir(service_path):
        item_path = os.path.join(service_path, item)
        if os.path.isdir(item_path) and (item.endswith("_config") or item == "config"):
            files_to_remove.append(item)
    
    for file_name in files_to_remove:
        file_path = os.path.join(service_path, file_name)
        if os.path.exists(file_path):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                print(f"✓ Xóa {file_name} cũ")
            except Exception as e:
                print(f"⚠️  Không thể xóa {file_name}: {e}")
    
    # Tạo Django project với cùng tên
    project_name = service_name
    cmd_create_project = f"python -m django startproject {project_name} ."
    
    if run_command(cmd_create_project, service_path):
        print(f"✓ Django project '{project_name}' tạo thành công")
    else:
        print(f"❌ Tạo Django project thất bại")
        return False
    
    # Tạo app API
    cmd_create_app = f"python manage.py startapp api"
    
    if run_command(cmd_create_app, service_path):
        print(f"✓ App 'api' tạo thành công")
    else:
        print(f"❌ Tạo app 'api' thất bại")
        return False
    
    return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🚀 KHỞI TẠO BOOKSTORE MICROSERVICES")
    print("="*60)
    
    successful = 0
    failed = 0
    
    # Kiểm tra Django đã cài đặt
    try:
        subprocess.run("python -m django --version", shell=True, check=True, capture_output=True)
        print("✓ Django đã cài đặt")
    except subprocess.CalledProcessError:
        print("❌ Django chưa cài đặt. Cài đặt Django trước!")
        sys.exit(1)
    
    # Tạo Django projects cho mỗi service
    for service in SERVICES:
        if create_django_project(service):
            successful += 1
        else:
            failed += 1
    
    # Kết quả
    print(f"\n{'='*60}")
    print(f"📊 KẾT QUẢ:")
    print(f"{'='*60}")
    print(f"✓ Thành công: {successful}/{len(SERVICES)}")
    print(f"❌ Thất bại: {failed}/{len(SERVICES)}")
    print(f"\nCấu trúc đã tạo tại: {BASE_DIR}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
