from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="rendering",
            label="Rendering",
            type=GroupType.CARD,
            children=[
                Option(
                    key="wined3d",
                    label="Use OpenGL-based wined3d instead of Vulkan-based DXVK",
                    tooltip="Use OpenGL-based wined3d for d3d11 and d3d10.",
                    env_key="PROTON_USE_WINED3D",
                    conflicts=["nod3d9", "nod3d10", "nod3d11", "nod3d12"],
                ),
                Option(
                    key="nod3d9",
                    label="Disable DX9",
                    env_key="PROTON_NO_D3D9",
                    condition=lambda s: not s.get("wined3d", False),
                ),
                Option(
                    key="nod3d10",
                    label="Disable DX10",
                    env_key="PROTON_NO_D3D10",
                    condition=lambda s: not s.get("wined3d", False),
                ),
                Option(
                    key="nod3d11",
                    label="Disable DX11",
                    env_key="PROTON_NO_D3D11",
                    condition=lambda s: not s.get("wined3d", False),
                ),
                Option(
                    key="nod3d12",
                    label="Disable DX12",
                    env_key="PROTON_NO_D3D12",
                    condition=lambda s: not s.get("wined3d", False),
                ),
            ],
        )
    ]
