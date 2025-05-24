from Mir import LanguageServer
from Mir.runtime import deno
from Mir.package_storage import PackageStorage

server_storage = PackageStorage(__package__, tag='0.0.1', sync_folder="./language-server")


class EslintLanguageServer(LanguageServer):
    name='eslint'
    activation_events={
        'selector': 'source.js, source.jsx, source.ts, source.tsx',
    }
    settings_file="Mir-eslint.sublime-settings"

    async def activate(self):
        await deno.setup()
        server_path = server_storage / "language-server" / "out" / 'eslintServer.js'
        # no "deno install" is required for Mir-eslint
        await self.connect('stdio', {
            'cmd': [deno.path, 'run', '-A', server_path, '--stdio']
        })
