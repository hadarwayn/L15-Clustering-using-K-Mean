"""
Enhanced K-Means GUI with clear instructions, pastel colors, and better visualization.
Replace your existing k_means_app.py with this version.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import os
from data_model import initialize_groups
from k_means_logic import run_kmeans, generate_explanation

# Pastel color palette (soft, pleasant colors)
COLORS = {
    'bg_main': '#F5F5F0',           # Soft cream
    'bg_control': '#E8F4F8',        # Pale blue
    'bg_results': '#FFF9E6',        # Soft yellow
    'button_explode': '#FFD4A3',    # Peach
    'button_kmeans': '#A8D5BA',     # Mint green
    'button_reset': '#FFB3BA',      # Soft pink
    'text_dark': '#2C3E50',         # Dark blue-gray
    'text_help': '#7F8C8D',         # Medium gray
    'accent': '#9B87B6',            # Soft purple
    'border': '#BDC3C7',            # Light gray
}

class KMeansApp(tk.Tk):
    """Enhanced K-Means Clustering Educational Simulator"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🎯 K-Means Clustering Interactive Simulator")
        self.geometry("1600x950")
        self.configure(bg=COLORS['bg_main'])
        
        # Ensure results directory exists
        os.makedirs('results', exist_ok=True)
        
        # Initialize data
        self.groups = initialize_groups()
        self.kmeans_results = None
        self.dragging_group = None
        self.drag_offset = None
        self.experiment_counter = 0
        
        # Create UI
        self.create_header()
        self.create_main_layout()
        
        # Initial plot
        self.plot_data()
        
    def create_header(self):
        """Create informative header with title and subtitle"""
        header_frame = tk.Frame(self, bg=COLORS['accent'], height=90)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🎯 K-Means Clustering Interactive Simulator",
            font=('Arial', 24, 'bold'),
            bg=COLORS['accent'],
            fg='white'
        )
        title.pack(pady=(10, 5))
        
        subtitle = tk.Label(
            header_frame,
            text="Drag groups, explode variance, and observe how K-Means clustering behaves • Educational Tool by AI Developer Expert Course",
            font=('Arial', 11),
            bg=COLORS['accent'],
            fg='white'
        )
        subtitle.pack()
        
    def create_main_layout(self):
        """Create main application layout"""
        main_container = tk.Frame(self, bg=COLORS['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Control Panel (Left)
        self.create_control_panel(main_container)
        
        # Visualization Canvas (Center-Right)
        self.create_visualization_panel(main_container)
        
        # Results Panel (Bottom)
        self.create_results_panel(main_container)
        
    def create_control_panel(self, parent):
        """Create enhanced control panel with clear instructions"""
        control_frame = tk.Frame(
            parent, 
            bg=COLORS['bg_control'], 
            width=350,
            relief=tk.RIDGE,
            borderwidth=2
        )
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        control_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            control_frame,
            text="🎮 CONTROLS",
            font=('Arial', 18, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark']
        )
        title_label.pack(pady=(15, 10))
        
        # Instruction text
        instruction_text = (
            "Follow these steps to explore\n"
            "how K-Means clustering works:"
        )
        instruction_label = tk.Label(
            control_frame,
            text=instruction_text,
            font=('Arial', 10),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT
        )
        instruction_label.pack(pady=(0, 15))
        
        # Step 1: Group Selection
        self.create_group_selector(control_frame)
        
        # Step 2: Drag Instructions
        self.create_drag_instructions(control_frame)
        
        # Step 3: Explode Controls
        self.create_explode_controls(control_frame)
        
        # Step 4: Run K-Means
        self.create_kmeans_controls(control_frame)
        
        # Step 5: Reset
        self.create_reset_controls(control_frame)
        
        # Status Panel
        self.create_status_panel(control_frame)
        
    def create_group_selector(self, parent):
        """Step 1: Group selection with explanation"""
        frame = tk.LabelFrame(
            parent,
            text="📍 STEP 1: Select a Group",
            font=('Arial', 11, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            relief=tk.GROOVE,
            borderwidth=2
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        help_text = (
            "Choose which group to manipulate.\n"
            "Each group is a cloud of colored points."
        )
        help_label = tk.Label(
            frame,
            text=help_text,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT,
            wraplength=300
        )
        help_label.pack(anchor=tk.W, padx=10, pady=(5, 10))
        
        self.selected_group_var = tk.StringVar(value="Group A")
        group_options = [g.label for g in self.groups]
        
        selector = ttk.Combobox(
            frame,
            textvariable=self.selected_group_var,
            values=group_options,
            state="readonly",
            font=('Arial', 11),
            width=20
        )
        selector.pack(padx=10, pady=(0, 10))
        
    def create_drag_instructions(self, parent):
        """Step 2: Drag instructions"""
        frame = tk.LabelFrame(
            parent,
            text="🖱️ STEP 2: Drag the Group",
            font=('Arial', 11, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            relief=tk.GROOVE,
            borderwidth=2
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        help_text = (
            "Click and drag the selected group's\n"
            "center (large X marker) on the plot\n"
            "to move it to a new position.\n\n"
            "💡 Try moving groups close together\n"
            "to see how K-Means handles overlap!"
        )
        help_label = tk.Label(
            frame,
            text=help_text,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT,
            wraplength=300
        )
        help_label.pack(anchor=tk.W, padx=10, pady=10)
        
    def create_explode_controls(self, parent):
        """Step 3: Explode variance controls"""
        frame = tk.LabelFrame(
            parent,
            text="💥 STEP 3: Explode Variance (Optional)",
            font=('Arial', 11, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            relief=tk.GROOVE,
            borderwidth=2
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        help_text = (
            "Increase the spread (variance) of the\n"
            "selected group to make it less dense.\n\n"
            "💡 Higher values scatter points more!"
        )
        help_label = tk.Label(
            frame,
            text=help_text,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT,
            wraplength=300
        )
        help_label.pack(anchor=tk.W, padx=10, pady=(5, 10))
        
        # Slider frame
        slider_frame = tk.Frame(frame, bg=COLORS['bg_control'])
        slider_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(
            slider_frame,
            text="Variance Multiplier:",
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark']
        ).pack(anchor=tk.W)
        
        self.variance_multiplier_var = tk.DoubleVar(value=2.0)
        
        slider = tk.Scale(
            slider_frame,
            from_=1.0,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.variance_multiplier_var,
            resolution=0.1,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            highlightbackground=COLORS['bg_control'],
            troughcolor='white'
        )
        slider.pack(fill=tk.X, pady=5)
        
        # Explode button
        explode_btn = tk.Button(
            frame,
            text="💥 Explode Selected Group",
            command=self.on_explode_clicked,
            font=('Arial', 11, 'bold'),
            bg=COLORS['button_explode'],
            fg=COLORS['text_dark'],
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            activebackground='#FFBF86'
        )
        explode_btn.pack(fill=tk.X, padx=10, pady=(5, 10))
        
    def create_kmeans_controls(self, parent):
        """Step 4: Run K-Means button"""
        frame = tk.LabelFrame(
            parent,
            text="🤖 STEP 4: Run Clustering",
            font=('Arial', 11, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            relief=tk.GROOVE,
            borderwidth=2
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        help_text = (
            "Execute K-Means algorithm to find\n"
            "3 clusters in your data. Watch how\n"
            "point edges change color based on\n"
            "their new cluster assignment!"
        )
        help_label = tk.Label(
            frame,
            text=help_text,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT,
            wraplength=300
        )
        help_label.pack(anchor=tk.W, padx=10, pady=(5, 10))
        
        run_btn = tk.Button(
            frame,
            text="🤖 Run K-Means (K=3)",
            command=self.on_run_kmeans_clicked,
            font=('Arial', 12, 'bold'),
            bg=COLORS['button_kmeans'],
            fg=COLORS['text_dark'],
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            activebackground='#8FC4A7'
        )
        run_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
        
    def create_reset_controls(self, parent):
        """Step 5: Reset button"""
        frame = tk.LabelFrame(
            parent,
            text="🔄 STEP 5: Reset",
            font=('Arial', 11, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            relief=tk.GROOVE,
            borderwidth=2
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        help_text = (
            "Start over with the original\n"
            "group positions and variances."
        )
        help_label = tk.Label(
            frame,
            text=help_text,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_help'],
            justify=tk.LEFT,
            wraplength=300
        )
        help_label.pack(anchor=tk.W, padx=10, pady=(5, 10))
        
        reset_btn = tk.Button(
            frame,
            text="🔄 Start Over",
            command=self.on_reset_clicked,
            font=('Arial', 11, 'bold'),
            bg=COLORS['button_reset'],
            fg=COLORS['text_dark'],
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            activebackground='#FF9FA5'
        )
        reset_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
        
    def create_status_panel(self, parent):
        """Status display panel"""
        frame = tk.LabelFrame(
            parent,
            text="📊 Status",
            font=('Arial', 10, 'bold'),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark']
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.status_var = tk.StringVar(value="Ready to start! Select a group and begin experimenting.")
        
        status_label = tk.Label(
            frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg=COLORS['bg_control'],
            fg=COLORS['text_dark'],
            wraplength=310,
            justify=tk.LEFT
        )
        status_label.pack(padx=10, pady=10, anchor=tk.W)
        
    def create_visualization_panel(self, parent):
        """Create matplotlib canvas for visualization"""
        canvas_frame = tk.Frame(parent, bg=COLORS['bg_main'])
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(11, 8))
        self.fig.patch.set_facecolor(COLORS['bg_main'])
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, canvas_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Connect mouse events for dragging
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        
    def create_results_panel(self, parent):
        """Create a resizable results explanation panel"""
        paned_window = tk.PanedWindow(parent, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg=COLORS['bg_main'])
        paned_window.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(10, 0))

        frame = tk.LabelFrame(
            paned_window,
            text="📈 K-Means Analysis Results",
            font=('Arial', 12, 'bold'),
            bg=COLORS['bg_results'],
            fg=COLORS['text_dark'],
            relief=tk.RIDGE,
            borderwidth=2
        )
        paned_window.add(frame, height=250) # Initial height

        self.results_text = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#FFFEF5',
            fg=COLORS['text_dark'],
            relief=tk.FLAT,
            borderwidth=5
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.insert('1.0', "Run K-Means to see detailed analysis here...")
        self.results_text.config(state=tk.DISABLED)

    def on_explode_clicked(self):
        """Handle explode button click"""
        selected_label = self.selected_group_var.get()
        scale_factor = self.variance_multiplier_var.get()
        
        target_group = next((g for g in self.groups if g.label == selected_label), None)
        
        if target_group:
            self.status_var.set(f"💥 Exploding {target_group.label} by {scale_factor:.1f}x...")
            self.config(cursor="watch")
            self.update()
            
            target_group.explode(scale_factor)
            self.plot_data()
            
            self.config(cursor="")
            self.status_var.set(f"✅ {target_group.label} variance increased by {scale_factor:.1f}x. Try running K-Means now!")
        else:
            self.status_var.set(f"❌ Error: Could not find {selected_label}")
            
    def on_run_kmeans_clicked(self):
        """Handle K-Means execution"""
        self.status_var.set("🤖 Running K-Means clustering...")
        self.config(cursor="watch")
        self.update()
        
        # Collect data
        all_points = np.vstack([g.points for g in self.groups])
        original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(self.groups)])
        
        # Run K-Means
        self.kmeans_results = run_kmeans(all_points, original_labels, n_clusters=3)
        
        # Generate explanation
        explanation = generate_explanation(self.groups, self.kmeans_results, original_labels)
        
        # Update UI
        self.plot_data()
        self.update_results_panel(explanation)
        self.save_results(explanation)
        
        self.config(cursor="")
        self.status_var.set(f"✅ K-Means complete! Silhouette Score: {self.kmeans_results['silhouette']:.3f}")
        
    def on_reset_clicked(self):
        """Reset to initial state"""
        self.status_var.set("🔄 Resetting to initial configuration...")
        
        self.groups = initialize_groups()
        self.kmeans_results = None
        
        self.update_results_panel(None)
        self.plot_data()
        
        self.selected_group_var.set("Group A")
        self.variance_multiplier_var.set(2.0)
        
        self.status_var.set("✅ Reset complete. Ready for a new experiment!")
        
    def on_mouse_press(self, event):
        """Handle mouse click for dragging"""
        if event.inaxes != self.ax:
            return
            
        click_point = np.array([event.xdata, event.ydata])
        
        for group in self.groups:
            distance = np.linalg.norm(click_point - group.mean)
            if distance < 0.8:  # Tolerance for clicking
                self.dragging_group = group
                self.drag_offset = group.mean - click_point
                self.status_var.set(f"🖱️ Dragging {group.label}... Release to place.")
                self.config(cursor="hand2")
                break
                
    def on_mouse_move(self, event):
        """Handle mouse movement while dragging"""
        if self.dragging_group is None or event.inaxes != self.ax:
            return
            
        new_mean = np.array([event.xdata, event.ydata]) + self.drag_offset
        
        # Boundary clipping
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        new_mean[0] = np.clip(new_mean[0], xlim[0], xlim[1])
        new_mean[1] = np.clip(new_mean[1], ylim[0], ylim[1])
        
        self.dragging_group.move(new_mean)
        self.plot_data()
        self.canvas.draw_idle()
        
    def on_mouse_release(self, event):
        """Handle mouse release after dragging"""
        if self.dragging_group:
            self.status_var.set(f"✅ {self.dragging_group.label} moved to new position. Run K-Means to see the effect!")
        self.dragging_group = None
        self.drag_offset = None
        self.config(cursor="")
        
    def plot_data(self):
        """Plot data with enhanced visualization"""
        self.ax.clear()
        
        # Set white background
        self.ax.set_facecolor('white')
        
        if self.kmeans_results:
            # After K-Means: show dual-color encoding
            cluster_colors = [g.color for g in self.groups]
            kmeans_labels = self.kmeans_results['labels']
            
            all_points = np.vstack([g.points for g in self.groups])
            original_labels = np.concatenate([[i] * g.n_points for i, g in enumerate(self.groups)])
            
            # Plot points with fill=original, edge=cluster
            for i in range(len(all_points)):
                orig_group_idx = original_labels[i]
                kmeans_cluster_idx = kmeans_labels[i]
                
                # The remapped labels should align, so the cluster index corresponds to the group index
                edge_color = cluster_colors[kmeans_cluster_idx]

                # Small filled dot for original group
                self.ax.scatter(
                    all_points[i, 0], all_points[i, 1],
                    c=self.groups[orig_group_idx].color,
                    s=15,  # Small dot
                    alpha=0.8,
                    edgecolor='none',
                    zorder=2
                )
                
                # Larger circle for cluster assignment
                self.ax.scatter(
                    all_points[i, 0], all_points[i, 1],
                    facecolor='none',
                    edgecolor=edge_color,
                    s=80,  # Larger circle
                    linewidth=2,
                    alpha=0.9,
                    zorder=1
                )
                
            # Plot K-Means centroids
            centroids = self.kmeans_results['centroids']
            self.ax.scatter(
                centroids[:, 0], centroids[:, 1],
                c='black',
                marker='X',
                s=350,
                edgecolor='white',
                linewidth=3,
                label="K-Means Centroid",
                zorder=10
            )
            
            title = "K-Means Clustering Results\n(Inner dot = Original Group, Outer circle = Assigned Cluster)"
        else:
            # Before K-Means: show only original groups
            for group in self.groups:
                self.ax.scatter(
                    group.points[:, 0], group.points[:, 1],
                    c=group.color,
                    label=group.label,
                    alpha=0.7,
                    s=40,
                    edgecolor='white',
                    linewidth=0.5
                )
            title = "Initial Data Distribution\n(Drag group centers to move them)"
            
        # Plot true means for all groups
        for group in self.groups:
            self.ax.scatter(
                group.mean[0], group.mean[1],
                c=group.color,
                marker='X',
                s=250,
                alpha=0.6,
                edgecolor='black',
                linewidth=2,
                label=f"{group.label} True Mean"
            )
            
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.ax.set_xlabel("Dimension 1 (X-axis)", fontsize=11)
        self.ax.set_ylabel("Dimension 2 (Y-axis)", fontsize=11)
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_aspect('equal', 'box')
        
        # Legend
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=9)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def update_results_panel(self, explanation):
        """Update results text panel"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        if explanation:
            self.results_text.insert(tk.END, explanation)
        else:
            self.results_text.insert(tk.END, "Run K-Means to see detailed analysis here...")
        self.results_text.config(state=tk.DISABLED)
        
    def save_results(self, explanation):
        """Save plot, explanation, and update README.md"""
        self.experiment_counter += 1
        
        # Save plot
        plot_filename = f"results/experiment_{self.experiment_counter}_plot.png"
        self.fig.savefig(plot_filename, dpi=150, bbox_inches='tight', facecolor='white')
        
        # Save explanation
        text_filename = f"results/experiment_{self.experiment_counter}_explanation.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(explanation)
            
        print(f"✅ Results saved: {plot_filename} and {text_filename}")

        # Update README.md
        with open("README.md", "a", encoding="utf-8") as f:
            f.write(f"\n\n## 🧪 Experiment {self.experiment_counter}\n\n")
            f.write(f"![Experiment {self.experiment_counter}](results/experiment_{self.experiment_counter}_plot.png)\n\n")
            f.write("### Analysis\n\n")
            f.write("```\n")
            f.write(explanation)
            f.write("\n```\n")
        print("✅ README.md updated with the new experiment.")

if __name__ == '__main__':
    app = KMeansApp()
    app.mainloop()
