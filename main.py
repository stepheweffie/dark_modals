from nicegui import ui


@ui.page(path='/')
async def dark_modals():

    modal = ui.element('modal').classes('rounded-lg shadow-lg').style(
                'min-width: 70%; z-index: 999; position: fixed;'
                )
    # The background modal will be styled with the dark mode
    bg_modal = ui.element('modal').classes('rounded-lg shadow-lg')
    # Modals can have alpha channel and work with dark mode
    modal_colors = {'bg_color': 'rgba(5, 255, 255, 0.9)', 'text_color': 'black',
                    'dark_bg_color': 'rgba(0, 0, 0, 0.9)', 'dark_text_color': 'white'}
    _bg_color = modal_colors['bg_color']
    dark_bg_color = modal_colors['dark_bg_color']
    _text_color = modal_colors['text_color']
    dark_text_color = modal_colors['dark_text_color']
    dark = ui.dark_mode(on_change=lambda v: set_modal_bg(dark_bg_color if v.value else _bg_color))
    dark_mode_switch = ui.switch('Dark Mode', value=False).classes('text-xl font-bold').props(
        'inline color=pink')
    dark_mode_switch.on('change', lambda e: toggle_dark_mode(e, bg_modal))
    dark_mode_switch.on('click', lambda e: dark.toggle())

    # Some background text
    ui.label('Dark Modals').classes('text-5xl text-center').style(
        'position: fixed; top: 25%; left: 40%;'
      )

    def set_modal_bg(color: str) -> None:
        ui.query('modal').style(replace=f'background-color: {color}')
        if color is dark_bg_color:
            ui.query('modal').style(replace=f'color: {dark_text_color}')
        else:
            ui.query('modal').style(replace=f'color: {_text_color}')

    def toggle_dark_mode(switch_state, _modal):
        bg_color = f'{dark_bg_color}' if switch_state is True else f'{_bg_color}'
        text_color = f'{dark_text_color}' if switch_state is True else f'{_text_color}'
        # Additional styles for the modal template
        _modal = ui.element('modal').classes('rounded-lg shadow-lg').style(
            'max-width: 100%; position: fixed; top: 25%; left: 40%;'
            f'z-index: 666; background-color: {bg_color}; color: {text_color};')
        return _modal

    async def try_submit(name, email, bg) -> None:
        if name and email:
            # await email validation
            bg_modal.remove(bg)
            ui.notify(f'Please Check {email}', color='positive')
        else:
            ui.notify('Please fill out all fields', color='negative')

    def get_modal():
        with bg_modal:
            # Without a new modal the modal will not close
            bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
        with modal and bg:
            # No KeyError when the modal is closed
            close = ui.icon('close').classes('text-2xl')
            close.on("click", lambda: bg_modal.remove(bg))
            content = ui.column().classes('mx-auto p-4')
            content.style(add='max-width: 100%;')
            with content:
                ui.label('Custom Modal').classes('text-2xl')
                with ui.row().classes('w-full items-center px-4'):
                    ui.label('Name').classes('text-xl')
                    name = ui.input(label='Name', placeholder='Enter Name')
                with ui.row().classes('w-full items-center px-4'):
                    ui.label('Email').classes('text-xl')
                    email = ui.input(label='Email', placeholder='Enter Email').on('keydown.enter', try_submit)
                with ui.row().classes('w-full items-center px-4'):
                    submit = ui.button('Submit').classes('text-xl w-72').on('click',
                                                                            lambda: try_submit(name.value, email.value,
                                                                                               bg))

    # Open the modals
    ui.button('Open Modal').on('click', get_modal)
    # await app.storage.user.get('authenticated', False)
    # if app.storage.user.get('authenticated', False):
    #     return RedirectResponse('/')


ui.run()

