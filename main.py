import flet as ft

def main(page: ft.Page):
    page.title = "My Greeting App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 500

    # I store the name here so I can use it on the next screen
    entered_name = ""

    name_input = ft.TextField(
        label="What is your name?",
        hint_text="Type your name here",
        width=280,
    )

    async def handle_continue_click(e):
        nonlocal entered_name

        # Stop here if nothing was typed, and show a popup instead
        if not name_input.value or not name_input.value.strip():
            popup = ft.AlertDialog(
                title=ft.Text("Oops!"),
                content=ft.Text("You need to type your name first."),
                actions=[
                    ft.TextButton("Got it", on_click=lambda _: page.close(popup))
                ],
            )
            page.open(popup)
            return

        entered_name = name_input.value.strip()
        await page.push_route("/greeting")

    async def handle_back_click(e):
        await page.push_route("/")

    def on_page_route_change(e):
        page.views.clear()

        # First screen - ask for the name
        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Text("Hi There!", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Let's get started."),
                        ft.Container(height=10),
                        name_input,
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Continue",
                            on_click=handle_continue_click,
                            width=280,
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        # Second screen - show the greeting
        elif page.route == "/greeting":
            page.views.append(
                ft.View(
                    route="/greeting",
                    controls=[
                        ft.Text(
                            f"Hello, {entered_name}!",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text("Nice to meet you."),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Back",
                            on_click=handle_back_click,
                            width=150,
                        ),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    page.on_route_change = on_page_route_change
    page.go("/")

ft.run(main)