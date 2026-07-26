import os

def fix_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

fix_file('backend/pyproject.toml', [
    ('[tool.ruff]\nselect', '[tool.ruff.lint]\nselect'),
])

fix_file('backend/app/database/migrations/env.py', [
    (
        '# Add app to path if needed (prepend_sys_path in alembic.ini covers this, but good practice)',
        '# Add app to path if needed\n# (prepend_sys_path in alembic.ini covers this, but good practice)'
    )
])

fix_file('backend/app/energyplus/interfaces.py', [
    (
        '    Abstract Base Class defining the contract for any simulation engine (e.g., EnergyPlus).',
        '    Abstract Base Class defining the contract for any simulation engine\n    (e.g., EnergyPlus).'
    ),
    (
        '    The AI and Digital Twin must only depend on this interface, never concrete implementations.',
        '    The AI and Digital Twin must only depend on this interface, never concrete\n    implementations.'
    )
])

fix_file('backend/app/energyplus/repository.py', [
    (
        '    def take_snapshot(self) -> Optional[SimulationSnapshot]:\n        """Creates a point-in-time snapshot of the current state and appends to history."""',
        '    def take_snapshot(self) -> Optional[SimulationSnapshot]:\n        """Creates a point-in-time snapshot of the current state and appends\n        to history."""'
    )
])

fix_file('backend/app/main.py', [
    (
        'description=(\n        "An autonomous AI platform that continuously monitors, reasons, "\n        "and optimizes smart building energy consumption "\n        "using EnergyPlus as a Digital Twin."\n    ),',
        'description="An autonomous AI platform.",'
    )
])

fix_file('backend/tests/unit/test_simulation_controller.py', [
    (
        '    controller.get_snapshot()\n    assert snapshot is not None',
        '    snapshot = controller.get_snapshot()\n    assert snapshot is not None'
    )
])

