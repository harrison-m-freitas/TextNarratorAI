import json
import requests
import typer
from pathlib import Path
from typing import Optional

try:
    import tiktoken
except ImportError:
    tiktoken = None

app = typer.Typer(help="Calcula custos da API OpenAI (GPT + TTS)")

MODEL_PRICING = {
    "gpt-4o":      {"input": 0.005,   "output": 0.02},
    "gpt-4.1":     {"input": 0.002,   "output": 0.008},
    "gpt-4.1-mini":{"input": 0.0004,  "output": 0.0016},
    "gpt-4.1-nano":{"input": 0.0001,  "output": 0.0004},
    "gpt-3.5":     {"input": 0.0005,  "output": 0.0015},
}
TTS_COST_PER_1000_CHARS = 0.015


def get_usd_to_brl_exchange_rate() -> Optional[float]:
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.json()["USDBRL"]["bid"])
    except Exception as error:
        typer.echo(f"⚠️  Erro ao obter cotação do dólar: {error}")
        return None


def count_tokens(text: str, model: str) -> int:
    if tiktoken:
        try:
            encoder = tiktoken.encoding_for_model(model)
        except Exception:
            encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))
    return max(1, len(text) // 4)


def calculate_cost(tokens_in: int, tokens_out: int, chars: int, model: str):
    prices = MODEL_PRICING[model]
    gpt_cost = (tokens_in / 1000) * prices["input"] + (tokens_out / 1000) * prices["output"]
    tts_cost = (chars / 1000) * TTS_COST_PER_1000_CHARS
    return gpt_cost, tts_cost, gpt_cost + tts_cost

def show_result(
    model: str, tokens_in: int, tokens_out: int, chars: int,
    gpt_cost: float, tts_cost: float, total_cost: float,
    output_format: str, exchange_rate: Optional[float] = None
):
    result = {
        "model": model,
        "tokens_input": tokens_in,
        "tokens_output": tokens_out,
        "chars_tts": chars,
        "cost_gpt": round(gpt_cost, 6),
        "cost_tts": round(tts_cost, 6),
        "total_cost_usd": round(total_cost, 6),
    }

    exchange_rate = exchange_rate or 1.00

    if output_format == "json":
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
        return

    typer.echo(f"\n📘 Modelo:         {model}")
    typer.echo(f"✍️  Tokens entrada: {tokens_in}")
    typer.echo(f"🧾 Tokens saída:   {tokens_out}")
    typer.echo(f"🔠 Caracteres TTS: {chars}")
    typer.echo(f"🧠 Custo GPT:      ${gpt_cost:.6f} - R$ {round(gpt_cost * exchange_rate, 6):.6f}")
    typer.echo(f"🎧 Custo TTS:      ${tts_cost:.6f} - R$ {round(tts_cost * exchange_rate, 6):.6f}")
    typer.echo(f"💰 Custo total:    ${total_cost:.6f} - R$ {round(total_cost * exchange_rate, 6):.6f}")


def validate_model(model: str) -> str:
    model = model.lower()
    if model not in MODEL_PRICING:
        raise typer.BadParameter(f"Modelo inválido. Escolha entre: {', '.join(MODEL_PRICING.keys())}")
    return model


def validate_output_format(fmt: str) -> str:
    fmt = fmt.lower()
    if fmt not in ["text", "json"]:
        raise typer.BadParameter("Formato inválido. Use 'text' ou 'json'.")
    return fmt

@app.command("calc")
def calculate_from_args(
    model: str = typer.Option("gpt-3.5", callback=validate_model, help="Modelo usado: " + ", ".join(MODEL_PRICING.keys())),
    input_tokens: int = typer.Option(..., help="Tokens de entrada (prompt)"),
    output_tokens: int = typer.Option(..., help="Tokens de saída (resposta)"),
    tts_chars: int = typer.Option(0, help="Caracteres usados para TTS"),
    output_format: str = typer.Option("text", "--format", "-f", callback=validate_output_format, help="Formato de saída (text/json)")
):
    gpt_cost, tts_cost, total = calculate_cost(input_tokens, output_tokens, tts_chars, model)
    exchange = get_usd_to_brl_exchange_rate()
    show_result(model, input_tokens, output_tokens, tts_chars, gpt_cost, tts_cost, total, output_format, exchange)


@app.command("calc-file")
def calculate_from_file(
    file_path: Path = typer.Argument(..., exists=True, help="Caminho para o arquivo .txt"),
    model: str = typer.Option("gpt-3.5", callback=validate_model, help="Modelo usado: " + ", ".join(MODEL_PRICING.keys())),
    auto_count: bool = typer.Option(False, "--auto-count", help="Contar tokens automaticamente"),
    input_tokens: Optional[int] = typer.Option(None, "--tokens-entrada", help="Tokens de entrada, se não usar --auto-count"),
    output_format: str = typer.Option("text", "--format", "-f", callback=validate_output_format, help="Formato de saída (text/json)")
):
    text = file_path.read_text(encoding="utf-8")
    char_count = len(text)

    if auto_count:
        if not tiktoken:
            typer.echo("❌ O modo automático requer o pacote 'tiktoken'. Instale com: pip install tiktoken")
            raise typer.Exit(code=1)
        input_tokens_count = count_tokens(text, model)
        output_tokens_count = input_tokens_count
    else:
        if input_tokens is None:
            typer.echo("❌ Informe --tokens-entrada ou use --auto-count")
            raise typer.Exit(code=1)
        input_tokens_count = input_tokens
        output_tokens_count = count_tokens(text, model)

    gpt_cost, tts_cost, total = calculate_cost(input_tokens_count, output_tokens_count, char_count, model)
    exchange = get_usd_to_brl_exchange_rate()
    show_result(model, input_tokens_count, output_tokens_count, char_count, gpt_cost, tts_cost, total, output_format, exchange)


if __name__ == "__main__":
    app()
