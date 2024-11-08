import constants


class GraphSceneProperties:
    def __init__(self,
                 use_edge_arrow: bool = False,
                 graph_hide_orphans: int = 0,
                 g_type: int = 0,
                 centrality_gradient: int = 0,
                 centrality_show_by: int = 0,
                 centrality_type: int = 0,
                 use_edge_label: bool = False,
                 node_label_color: str = "#000000",  # Default to black
                 node_highlight_color: str = "#FF0000",  # Default to red
                 node_background_color: str = "#FFFFFF",  # Default to white
                 node_foreground_color: str = "#000000",  # Default to black
                 node_shape_style: str = "circle",  # Default shape
                 node_font_size: int = 12,  # Default font size
                 label_position: int = 0,  # Default position
                 image_height: int = 30,  # Default height
                 image_width: int = 30,  # Default width
                 show_node_label: bool = True,
                 use_node_icon: bool = True,
                 use_node_image: bool = False,
                 edge_font_size: int = 12,
                 application_icon_size: constants.ApplicationIconSize = constants.ApplicationIconSize.Small):  # Default edge font size
        self.use_edge_arrow = use_edge_arrow
        self.graph_hide_orphans = graph_hide_orphans
        self.g_type = g_type
        self.centrality_gradient = centrality_gradient
        self.centrality_show_by = centrality_show_by
        self.centrality_type = centrality_type
        self.use_edge_label = use_edge_label
        self.node_label_color = node_label_color
        self.node_highlight_color = node_highlight_color
        self.node_background_color = node_background_color
        self.node_foreground_color = node_foreground_color
        self.node_shape_style = node_shape_style
        self.node_font_size = node_font_size
        self.label_position = label_position
        self.image_height = image_height
        self.image_width = image_width
        self.show_node_label = show_node_label
        self.use_node_icon = use_node_icon
        self.use_node_image = use_node_image
        self.edge_font_size = edge_font_size
        self.application_icon_size = application_icon_size

    def __repr__(self):
        return (f"GraphSceneProperties(use_edge_arrow={self.use_edge_arrow}, "
                f"graph_hide_orphans={self.graph_hide_orphans}, "
                f"g_type={self.g_type}, "
                f"centrality_gradient={self.centrality_gradient}, "
                f"centrality_show_by={self.centrality_show_by}, "
                f"centrality_type={self.centrality_type}, "
                f"use_edge_label={self.use_edge_label}, "
                f"node_label_color='{self.node_label_color}', "
                f"node_highlight_color='{self.node_highlight_color}', "
                f"node_background_color='{self.node_background_color}', "
                f"node_foreground_color='{self.node_foreground_color}', "
                f"node_shape_style='{self.node_shape_style}', "
                f"node_font_size={self.node_font_size}, "
                f"label_position={self.label_position}, "
                f"image_height={self.image_height}, "
                f"image_width={self.image_width}, "
                f"show_node_label={self.show_node_label}, "
                f"use_node_icon={self.use_node_icon}, "
                f"use_node_image={self.use_node_image}, "
                f"edge_font_size={self.edge_font_size})")
