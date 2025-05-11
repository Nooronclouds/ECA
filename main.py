from database import (
    get_product_details,
    add_alternative_product
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def display_product_details(product):
    """Show formatted product info"""
    table = Table(title="Product Details", show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    
    table.add_row("Name", product['product_name'])
    table.add_row("Type", product['product_type'])
    table.add_row("Brand", product['brand_name'])
    table.add_row("Status", "[red]Affiliated" if product['is_affiliated'] else "[green]Clean")
    table.add_row("Countries", product.get('countries', 'Unknown'))
    
    console.print(Panel.fit(table))
    if product.get('bds_report'):
        console.print(f"BDS Report: [link={product['bds_report']}]View Report[/link]")

def main():
    while True:
        try:
            console.print("\n[bold cyan]=== Boycott Manager ===")
            search_term = input("Enter product to check (or 'quit' to exit): ")
            
            if search_term.lower() == 'quit':
                break
                
            products = get_product_details(search_term)
            if not products:
                console.print("[yellow]No matching products found.[/yellow]")
                continue
                
            product = products[0]  # Show first match
            display_product_details(product)
            
            # Action menu
            console.print("\n[bold]Actions:[/bold]")
            console.print("1. Add alternative product")
            console.print("2. New search")
            
            choice = input("Select action (1-2): ")
            if choice == "1":
                alt_name = input("Alternative product name: ")
                alt_brand = input("Brand name (press Enter if same): ") or None
                user_id = input("Enter your user ID: ")  # Should be validated
                if add_alternative_product(user_id, product['product_id'], alt_name, alt_brand):
                    console.print("[green]✓ Alternative saved![/green]")
                else:
                    console.print("[red]Failed to save alternative[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()