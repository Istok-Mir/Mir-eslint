from Mir import LanguageServer, electron_node_20, PackageStorage


server_storage = PackageStorage(tag='0.0.1')
server_path = server_storage / "language-server" / "out" / 'eslintServer.js'

async def package_storage_setup():
    if server_path.exists():
        return
    await electron_node_20.setup()
    server_storage.copy("./language-server")
    with LoaderInStatusBar(f'installing eslint'):
        await command([deno.path, "install"], cwd=str(server_storage / "language-server"))

class EslintLanguageServer(LanguageServer):
    name='eslint'
    activation_events={
        'selector': 'source.js, source.jsx, source.ts, source.tsx',
    }
    settings_file="Mir-eslint.sublime-settings"

    async def activate(self):
        # setup runtime and install dependencies
        await package_storage_setup()

        self.settings.set('workspaceFolder', self.initialize_params.get('workspaceFolders', [])[0])

        def handle_status(_):
            ...

        self.on_notification('eslint/status', handle_status)
        await self.connect('stdio', {
            'cmd': [electron_node_20.path, server_path, '--stdio']
        })
