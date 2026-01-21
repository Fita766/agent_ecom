"""
Script pour corriger les imports BaseTool vers StructuredTool
"""
import re
from pathlib import Path

tools_dir = Path("tools")
tool_files = [
    "aliexpress_scraper.py",
    "amazon_scraper.py",
    "google_trends.py",
    "pinterest_scraper.py",
    "tiktok_scraper.py",
    "shopify_tool.py",
    "duplicate_checker_tool.py"
]

for tool_file in tool_files:
    file_path = tools_dir / tool_file
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer l'import
        content = content.replace(
            "from crewai_tools import BaseTool",
            "from langchain_core.tools import StructuredTool"
        )
        
        # Remplacer BaseTool par StructuredTool dans la classe
        content = re.sub(
            r'class (\w+)\(BaseTool\):',
            r'class \1(StructuredTool):',
            content
        )
        
        # Pour StructuredTool, on doit changer la structure
        # Au lieu de name, description, args_schema, _run
        # On utilise name, description, args_schema, func
        
        # Trouver la classe et modifier
        lines = content.split('\n')
        new_lines = []
        in_class = False
        class_name = None
        has_run_method = False
        
        for i, line in enumerate(lines):
            if 'class ' in line and 'StructuredTool' in line:
                in_class = True
                class_name = line.split('class ')[1].split('(')[0]
                new_lines.append(line)
            elif in_class and 'def _run(' in line:
                # Remplacer _run par une fonction normale
                func_name = line.split('def _run(')[1].split(')')[0]
                # Extraire les paramètres
                params = line.split('def _run(')[1].split(')')[0]
                # Créer une fonction normale
                new_lines.append(f"    def _run({params}):")
                has_run_method = True
            elif in_class and line.strip().startswith('name: str ='):
                # Garder name mais pas comme attribut de classe
                continue
            elif in_class and line.strip().startswith('description: str ='):
                # Garder description mais pas comme attribut de classe
                continue
            elif in_class and line.strip().startswith('args_schema: Type[BaseModel] ='):
                # Garder args_schema mais pas comme attribut de classe
                continue
            else:
                new_lines.append(line)
        
        # Pour StructuredTool, on doit créer une instance à la fin
        # Chercher la fin de la classe et ajouter la création d'instance
        if has_run_method:
            # Trouver où créer l'instance
            for i in range(len(new_lines) - 1, -1, -1):
                if 'return results' in new_lines[i] or 'return {' in new_lines[i]:
                    # Ajouter la création de l'instance après la classe
                    indent = '    '
                    instance_code = f"""
def create_{class_name.lower()}():
    return StructuredTool(
        name="{class_name.replace('Tool', '')}",
        description="",
        args_schema={class_name.replace('Tool', '')}Input,
        func={class_name.lower().replace('tool', '')}_func
    )

def {class_name.lower().replace('tool', '')}_func(product_name: str, max_results: int = 5):
    tool = {class_name}()
    return tool._run(product_name, max_results)
"""
                    # Insérer après la classe
                    # Trouver la fin de la classe (ligne vide ou nouvelle classe)
                    for j in range(i, len(new_lines)):
                        if j == len(new_lines) - 1 or (new_lines[j].strip() == '' and j > i + 5):
                            new_lines.insert(j + 1, instance_code)
                            break
                    break
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ {tool_file} corrigé")

print("Migration terminée!")
