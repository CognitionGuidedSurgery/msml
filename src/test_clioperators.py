import msml.api.clisupport as cli
import msml.frontend as F


cli.consolecatcher._reset_stdio()
app = F.App()
cli.OperatorAsCLI.generate_all(app.alphabet, "/tmp")
