# File: src/k_means_app.py
"""
GUI Controller for the K-Means Clustering Educational Simulator.
Based on PRD FR2 and Phase 2 Tasks.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from data_model import initialize_groups
from k_means_logic import run_kmeans, generate_explanation

class KMeansApp(tk.Tk):
    """
    Main application class for the K-Means simulator.
    It orchestrates the GUI, data, and logic.
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("L15 - K-Means Clustering Educational Simulator")
        self.geometry("1400x900")
        
        # --- Data Initialization (Task P2-T1.3) ---
        self.groups = initialize_groups()
        self.kmeans_results = None
        self.experiment_counter = 0
        
        # --- GUI Structure (Task P2-T1.2) ---
        self.create_layout()
        
        # --- Initial Plot (Task P2-T3.3) ---
        self.plot_data()

    def save_results(self, explanation):
        """Saves the current plot and explanation to the results folder."""
        self.experiment_counter += 1
        
        # Save plot
        plot_filename = f"results/experiment_{self.experiment_counter}_plot.png"
        self.fig.savefig(plot_filename, bbox_inches='tight')
        
        # Save explanation
        explanation_filename = f"results/experiment_{self.experiment_counter}_explanation.txt"
        with open(explanation_filename, "w") as f:
            f.write(explanation)
            
        self.status_var.set(f"Results saved to experiment_{self.experiment_counter}")

    def create_layout(self):
        """Creates the main frames for the application layout."""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Control Panel (Left) ---
        control_frame = ttk.LabelFrame(main_frame, text="Controls", width=250)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False) # Prevent resizing

        # --- Visualization (Center) ---
        canvas_frame = ttk.LabelFrame(main_frame, text="Visualization")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Results (Bottom) ---
        # This will be added later, for now we just have the two main frames.
        # A bottom frame would require a different layout approach.
        # We will place the results panel inside the control frame for now.
        
        self.create_control_widgets(control_frame)
        self.create_canvas(canvas_frame)

    def create_control_widgets(self, parent):
        """Creates the widgets for the control panel."""
        
        # Make widgets expand
        parent.grid_columnconfigure(0, weight=1)

        # --- Group Selector (Task P2-T2.1) ---
        group_selector_frame = ttk.LabelFrame(parent, text="1. Select Group")
        group_selector_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.selected_group_var = tk.StringVar(value="Group A")
        group_options = [g.label for g in self.groups]
        group_selector = ttk.Combobox(
            group_selector_frame, 
            textvariable=self.selected_group_var, 
            values=group_options,
            state="readonly"
        )
        group_selector.pack(fill=tk.X, padx=5, pady=5)

        # --- Explosion Controls (Task P2-T2.2 & P2-T2.5) ---
        explode_frame = ttk.LabelFrame(parent, text="2. Explode Variance")
        explode_frame.pack(fill=tk.X, padx=5, pady=5)

        self.variance_multiplier_var = tk.DoubleVar(value=2.0)
        variance_slider = ttk.Scale(
            explode_frame,
            from_=1.0,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.variance_multiplier_var,
        )
        variance_slider.pack(fill=tk.X, padx=5, pady=5)
        
        explode_button = ttk.Button(
            explode_frame, 
            text="Explode Selected Group",
            command=self.on_explode_clicked
        )
        explode_button.pack(fill=tk.X, padx=5, pady=5)

        # --- K-Means Controls (Task P2-T2.3) ---
        kmeans_frame = ttk.LabelFrame(parent, text="3. Run Clustering")
        kmeans_frame.pack(fill=tk.X, padx=5, pady=5)
        
        run_button = ttk.Button(
            kmeans_frame, 
            text="Run K-Means (K=3)",
            command=self.on_run_kmeans_clicked
        )
        run_button.pack(fill=tk.X, padx=5, pady=5)

        # --- Reset Controls (Task P2-T2.4) ---
        reset_frame = ttk.LabelFrame(parent, text="4. Reset")
        reset_frame.pack(fill=tk.X, padx=5, pady=5)
        
        reset_button = ttk.Button(
            reset_frame, 
            text="Start Over",
            command=self.on_reset_clicked
        )
        reset_button.pack(fill=tk.X, padx=5, pady=5)

        # --- Status Label (Task P2-T2.6) ---
        status_frame = ttk.LabelFrame(parent, text="Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        self.status_var = tk.StringVar(value="Application started.")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, wraplength=230)
        status_label.pack(fill=tk.X, padx=5, pady=5)

        # --- Results Panel (Task P2-T4) ---
        results_frame = ttk.LabelFrame(parent, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD, state="disabled", font=("Courier", 9))
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

    def on_explode_clicked(self):
        """Handles the 'Explode' button click event."""
        selected_label = self.selected_group_var.get()
        scale_factor = self.variance_multiplier_var.get()
        
        target_group = None
        for g in self.groups:
            if g.label == selected_label:
                target_group = g
                break
        
        if target_group:
            self.status_var.set(f"Exploding {target_group.label} by {scale_factor:.1f}x...")
            self.config(cursor="watch")
            self.update()

            target_group.explode(scale_factor)
            self.plot_data()
            
            self.config(cursor="")
            self.status_var.set(f"{target_group.label} exploded.")
        else:
            self.status_var.set(f"Error: Could not find {selected_label}.")

    def on_run_kmeans_clicked(self):
        """Handles the 'Run K-Means' button click event."""
        self.status_var.set("Running K-Means (K=3)...")
        self.config(cursor="watch")
        self.update() # Force GUI to update

        # 1. Collect all data points
        all_points = np.vstack([g.points for g in self.groups])
        original_labels = np.concatenate([
            [i] * g.n_points for i, g in enumerate(self.groups)
        ])

        # 2. Run K-Means
        self.kmeans_results = run_kmeans(all_points, n_clusters=3)

        # 3. Generate Explanation
        explanation = generate_explanation(self.groups, self.kmeans_results, original_labels)

        # 4. Update GUI
        self.plot_data() # Re-plot with K-Means results
        self.update_results_panel(explanation)
        
        # 5. Save Results
        self.save_results(explanation)
        
        self.config(cursor="")
        self.status_var.set("K-Means clustering complete.")

    def update_results_panel(self, explanation: str | None):
        """Updates the text in the results panel."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        if explanation:
            self.results_text.insert(tk.END, explanation)
        self.results_text.config(state="disabled")

    def on_reset_clicked(self):
        """Resets the application to its initial state."""
        self.status_var.set("Resetting to initial configuration...")
        
        # Re-initialize data
        self.groups = initialize_groups()
        self.kmeans_results = None
        
        # Clear results panel
        self.update_results_panel(None)
        
        # Re-plot
        self.plot_data()
        
        # Reset UI elements
        self.selected_group_var.set("Group A")
        self.variance_multiplier_var.set(2.0)
        
        self.status_var.set("Reset complete.")
        self.canvas.draw()

    def create_canvas(self, parent):
        """Creates the Matplotlib canvas and toolbar."""
        # --- Matplotlib Figure (Task P2-T1.4) ---
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.tight_layout(pad=3.0)

        # --- Canvas (Task P2-T3.1) ---
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Toolbar (Task P2-T3.2) ---
        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Event Handling for Drag-and-Drop (Task P3-T3) ---
        self.dragging_group = None
        self.drag_offset = None
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)

    def on_mouse_press(self, event):
        """Handles mouse clicks on the canvas to initiate dragging."""
        if event.inaxes != self.ax:
            return
        
        # Check if a group's mean is clicked
        click_point = np.array([event.xdata, event.ydata])
        for i, group in enumerate(self.groups):
            distance = np.linalg.norm(click_point - group.mean)
            # Use a tolerance for clicking near the mean
            if distance < 0.5: # Adjust tolerance as needed
                self.dragging_group = group
                self.drag_offset = group.mean - click_point
                self.status_var.set(f"Dragging {group.label}...")
                self.config(cursor="hand2")
                break

    def on_mouse_move(self, event):
        """Handles mouse movement to drag a group."""
        if self.dragging_group is None or event.inaxes != self.ax:
            return
        
        new_mean = np.array([event.xdata, event.ydata]) + self.drag_offset
        
        # Boundary Clipping (Task P3-T3.5)
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        new_mean[0] = np.clip(new_mean[0], xlim[0], xlim[1])
        new_mean[1] = np.clip(new_mean[1], ylim[0], ylim[1])
        
        self.dragging_group.move(new_mean)
        self.plot_data()
        self.canvas.draw_idle()

    def on_mouse_release(self, event):
        """Handles mouse release to end dragging."""
        if self.dragging_group:
            self.status_var.set(f"{self.dragging_group.label} moved.")
        self.dragging_group = None
        self.drag_offset = None
        self.config(cursor="")


    def plot_data(self):
        """
        Plots the Gaussian groups on the canvas.
        Handles dual-color plotting if K-Means has been run.
        """
        self.ax.clear()
        
        all_points = np.vstack([g.points for g in self.groups])
        
        # --- Plotting based on whether K-Means has run ---
        if self.kmeans_results:
            # Dual-Color Plotting (Task P3-T1)
            cluster_colors = ['#E69F00', '#56B4E9', '#009E73']
            kmeans_labels = self.kmeans_results['labels']
            
            # Plot each point with original fill and cluster edge
            for i, group in enumerate(self.groups):
                start_index = sum(g.n_points for g in self.groups[:i])
                end_index = start_index + group.n_points
                
                self.ax.scatter(
                    group.points[:, 0], group.points[:, 1],
                    facecolor=group.color,
                    edgecolor=[cluster_colors[l] for l in kmeans_labels[start_index:end_index]],
                    linewidth=1.5,
                    label=f"Group {group.label}",
                    alpha=0.8,
                    s=50 # Slightly larger to show edges
                )
        else:
            # Initial plot (no K-Means results yet)
            for group in self.groups:
                self.ax.scatter(
                    group.points[:, 0], group.points[:, 1],
                    c=group.color,
                    label=f"Group {group.label}",
                    alpha=0.6,
                    edgecolor='none'
                )

        # --- Plot True Means and Centroids ---
        for group in self.groups:
            self.ax.scatter(
                group.mean[0], group.mean[1],
                c=group.color,
                marker='X', s=200,
                edgecolor='black',
                label=f"{group.label} True Mean"
            )
            
        if self.kmeans_results:
            # Plot K-Means Centroids (Task P3-T2)
            centroids = self.kmeans_results['centroids']
            self.ax.scatter(
                centroids[:, 0], centroids[:, 1],
                c='black',
                marker='X', s=250,
                edgecolor='white',
                linewidth=2,
                label="K-Means Centroid",
                zorder=10
            )
            self.ax.set_title("K-Means Clustering Results")
        else:
            self.ax.set_title("Initial Data Distribution")
            
        self.ax.set_xlabel("Dimension 1")
        self.ax.set_ylabel("Dimension 2")
        
        # Create a legend that doesn't have duplicate entries
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.25, 1))
        
        self.ax.grid(True)
        self.ax.set_aspect('equal', 'box')
        
        self.canvas.draw()

if __name__ == '__main__':
    app = KMeansApp()
    app.mainloop()
