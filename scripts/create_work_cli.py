import sys
import shutil
import typer
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.utils.normalizer import normalize_work_id
from core.utils.file_utils import save_json, load_json

app = typer.Typer(help="Ferramentas para registrar obras literárias no sistema.")

BASE_INPUT = Path("data/input")
BASE_STORE = Path("data/store")
BASE_OUTPUT = Path("data/output")


@app.command("create")
def create_work(
    title: str = typer.Argument(..., help="Título da obra (ex: Urban Strengthening System)"),
    original_language: str = typer.Option("zh-CN", "--lang", "-l", help="Idioma original da obra (ex: zh-CN, en, pt-BR)"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="Nome do autor (opcional)"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Lista de tags separadas por vírgula (opcional)")
):
    """
    Cria a estrutura de pastas, metadata e arquivos iniciais para uma nova obra.
    """
    work_id = normalize_work_id(title)
    input_dir = BASE_INPUT / work_id / "chapters"
    store_dir = BASE_STORE / work_id
    output_dir = BASE_OUTPUT / work_id

    input_dir.mkdir(parents=True, exist_ok=True)
    store_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "title": title,
        "original_language": original_language,
        "author": author or "Desconhecido",
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
    }
    
    save_json(BASE_INPUT / work_id / "metadata.json", metadata)
    save_json(store_dir / "manifest.json", {"chapters": {}})

    typer.echo(f"✅ Obra '{title}' registrada com sucesso.")
    typer.echo(f"work_id: {work_id}")
    typer.echo(f"📂 Pastas criadas: input/, store/, output/")
    typer.echo(f"📄 metadata.json e manifest.json prontos.")
    typer.echo(f"Adicione capítulos em: data/input/{work_id}/chapters/")


@app.command("list")
def list_works():
    """
    Lista todas as obras registradas com seus metadados.
    """
    if not BASE_INPUT.exists():
        typer.echo("Nenhuma obra encontrada.")
        raise typer.Exit()

    for work_dir in sorted(BASE_INPUT.iterdir()):
        metadata_path = work_dir / "metadata.json"
        if metadata_path.exists():
            metadata = load_json(metadata_path)
            typer.echo(f"\n📘 {metadata.get('title')} ({work_dir.name})")
            typer.echo(f"   Idioma: {metadata.get('original_language')}")
            typer.echo(f"   Autor: {metadata.get('author')}")
            typer.echo(f"   Tags : {', '.join(metadata.get('tags', []))}")
        else:
            typer.echo(f"\n📁 {work_dir.name} (sem metadata.json)")


@app.command("update")
def update_work(
    work_id: str = typer.Argument(..., help="ID da obra (pasta na input/)"),
    title: Optional[str] = typer.Option(None, "--title"),
    original_language: Optional[str] = typer.Option(None, "--lang", "-l"),
    author: Optional[str] = typer.Option(None, "--author", "-a"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t")
):
    """
    Atualiza os metadados de uma obra existente.
    """
    metadata_path = BASE_INPUT / work_id / "metadata.json"
    if not metadata_path.exists():
        typer.echo("❌ metadata.json não encontrado para essa obra.")
        raise typer.Exit()

    metadata = load_json(metadata_path)

    if title:
        metadata["title"] = title
    if original_language:
        metadata["original_language"] = original_language
    if author:
        metadata["author"] = author
    if tags:
        metadata["tags"] = [t.strip() for t in tags.split(",")]

    save_json(metadata_path, metadata)
    typer.echo(f"✅ Metadados de '{work_id}' atualizados com sucesso.")

@app.command("list-chapters")
def list_chapters(work_id: str = typer.Argument(..., help="ID da obra")):
    """
    Lista os capítulos .txt da obra e mostra se foram processados (com base no manifest).
    """
    chapters_dir = BASE_INPUT / work_id / "chapters"
    manifest_path = BASE_STORE / work_id / "manifest.json"
    
    if not chapters_dir.exists():
        typer.echo("❌ Obra não encontrada.")
        raise typer.Exit()
    
    manifest = {}
    if manifest_path.exists():
        manifest = load_json(manifest_path).get("chapters", {})
        
    txt_files = sorted(chapters_dir.glob("*.txt"))
    if not txt_files:
        typer.echo("📂 Nenhum capítulo encontrado.")
        return

    typer.echo(f"📑 Capítulos em '{work_id}':\n")
    for f in txt_files:
        chapter_id = f.stem
        status = "✅ processado" if chapter_id in manifest else "❌ pendente"
        typer.echo(f"  {chapter_id}.txt  → {status}")

    typer.echo(f"\nTotal: {len(txt_files)} capítulo(s)")
    
@app.command("delete-work")
def delete_work(
    work_id: str = typer.Argument(..., help="ID da obra a ser removida"),
    yes: bool = typer.Option(False, "--yes", help="Confirma a exclusão irreversível")
):
    """
    Deleta todos os dados da obra (input, store, output). Requer --yes para confirmar.
    """
    if not yes:
        typer.echo("⚠️  Esta ação removerá permanentemente a obra!")
        typer.echo("Use --yes para confirmar.")
        raise typer.Exit()

    paths = [
        BASE_INPUT / work_id,
        BASE_STORE / work_id,
        BASE_OUTPUT / work_id,
    ]

    for p in paths:
        if p.exists():
            shutil.rmtree(p)
            typer.echo(f"🗑️  Removido: {p}")

    typer.echo(f"✅ Obra '{work_id}' removida com sucesso.")


if __name__ == "__main__":
    app()
