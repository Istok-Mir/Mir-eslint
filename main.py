from Mir import LanguageServer, electron_node_20, PackageStorage


server_storage = PackageStorage(tag='0.0.1', sync_folder="./language-server")


class EslintLanguageServer(LanguageServer):
    name='eslint'
    activation_events={
        'selector': 'source.js, source.jsx, source.ts, source.tsx',
    }
    settings_file="Mir-eslint.sublime-settings"

    async def activate(self):
        await electron_node_20.setup()
        server_path = server_storage / "language-server" / "out" / 'eslintServer.js'
        self.settings.set('workspaceFolder', self.initialize_params.get('workspaceFolders', [])[0])

        def handle_status(_):
            ...

        self.on_notification('eslint/status', handle_status)
        await self.connect('stdio', {
            'cmd': [electron_node_20.path, server_path, '--stdio']
        })
