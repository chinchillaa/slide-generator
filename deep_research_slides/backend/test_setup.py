#!/usr/bin/env python3
"""
セットアップと依存関係のテストスクリプト
"""

import sys
from pathlib import Path

def check_import(module_name, package_name=None):
    """モジュールのインポートをテスト"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def check_env_vars():
    """環境変数の確認"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    env_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "HF_TOKEN": "Hugging Face Token",
        "SERPER_API_KEY": "Serper API Key (or SERPAPI_API_KEY)",
        "SERPAPI_API_KEY": "SerpAPI Key (or SERPER_API_KEY)"
    }
    
    print("\n=== Environment Variables ===")
    has_search_api = False
    
    for var, desc in env_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            if var in ["SERPER_API_KEY", "SERPAPI_API_KEY"]:
                has_search_api = True
            print(f"✅ {var} is set ({desc})")
        else:
            if var in ["SERPER_API_KEY", "SERPAPI_API_KEY"] and has_search_api:
                continue  # 片方があればOK
            print(f"❌ {var} is NOT set ({desc})")

def check_smolagents():
    """smolagentsのインストール確認"""
    smolagents_path = Path(__file__).parent.parent.parent / "smolagents"
    sys.path.insert(0, str(smolagents_path))
    
    try:
        import smolagents
        print(f"✅ smolagents is available")
        return True
    except ImportError:
        print(f"❌ smolagents is NOT available at {smolagents_path}")
        return False

def main():
    print("=== Deep Research Slides Setup Check ===\n")
    
    print("=== Required Python Packages ===")
    packages = [
        ("fastapi", None),
        ("uvicorn", None),
        ("dotenv", "python-dotenv"),
        ("pydantic", None),
        ("websockets", None),
        ("anthropic", None),
        ("bs4", "beautifulsoup4"),
        ("google_search_results", None),
        ("huggingface_hub", None),
        ("openai", None),
        ("PIL", "pillow"),
        ("requests", None),
        ("transformers", None),
        ("jinja2", None),
        ("markdown", None),
    ]
    
    all_ok = True
    for module, package in packages:
        if not check_import(module, package):
            all_ok = False
    
    print("\n=== smolagents ===")
    if not check_smolagents():
        all_ok = False
    
    check_env_vars()
    
    if all_ok:
        print("\n✅ All dependencies are installed!")
        print("You can now run the application with:")
        print("  python3 run.py")
    else:
        print("\n❌ Some dependencies are missing.")
        print("Please install them using:")
        print("  pip3 install -r requirements.txt")
        print("  pip3 install -e ../../smolagents/[dev]")

if __name__ == "__main__":
    main()