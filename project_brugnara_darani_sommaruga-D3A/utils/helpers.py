def create_biomechanics_animation(model_results, merged_df, last_rep, muscle_columns=None, force_columns=None, interval=400, window=50):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from IPython.display import HTML
    
    if muscle_columns is None:
        muscle_columns = ['aDEL', 'pDEL', 'lBIC', 'sBIC', 'lTRI', 'BRA', 'mPEC']
    if force_columns is None:
        force_columns = ['force_x', 'force_y']
    
    best_model_name = min(model_results.items(), key=lambda x: x[1]["RMSE"])[0]
    best_predictions = model_results[best_model_name]['predictions']
    
    test_data = merged_df[merged_df['repetition'] == last_rep]
    actual_force = test_data[force_columns].values
    muscle_data = test_data[muscle_columns].values
    pred_force = best_predictions
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3)
    
    # Arm movement (force vector from origin)
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_xlim(-30, 30)
    ax0.set_ylim(-30, 30)
    ax0.set_aspect('equal')
    ax0.set_title('Arm Movement (Force Vector)')
    ax0.set_xlabel('X (N)')
    ax0.set_ylabel('Y (N)')
    ax0.grid(True)
    arm_line_actual, = ax0.plot([], [], 'bo-', lw=3, label='Actual')
    arm_line_pred, = ax0.plot([], [], 'ro--', lw=2, alpha=0.6, label='Predicted')
    ax0.legend()
    
    # Muscle activation bars
    ax1 = fig.add_subplot(gs[0, 1])
    bar_positions = np.arange(len(muscle_columns))
    bars = ax1.bar(bar_positions, np.zeros(len(muscle_columns)), color='skyblue')
    ax1.set_ylim(0, 0.05)
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(muscle_columns, rotation=45)
    ax1.set_title('Muscle Activation')
    ax1.set_ylabel('Activation (mV)')
    
    # Force X over time
    ax2 = fig.add_subplot(gs[1, 0])
    line_fx_actual, = ax2.plot([], [], 'b-', label='Actual X')
    line_fx_pred, = ax2.plot([], [], 'r--', label='Predicted X')
    ax2.set_xlim(0, window)
    ax2.set_ylim(-30, 30)
    ax2.set_title('Force X over Time')
    ax2.set_ylabel('Force X (N)')
    ax2.legend()
    ax2.grid(True)
    
    # Force Y over time
    ax3 = fig.add_subplot(gs[1, 1])
    line_fy_actual, = ax3.plot([], [], 'b-', label='Actual Y')
    line_fy_pred, = ax3.plot([], [], 'r--', label='Predicted Y')
    ax3.set_xlim(0, window)
    ax3.set_ylim(-30, 30)
    ax3.set_title('Force Y over Time')
    ax3.set_ylabel('Force Y (N)')
    ax3.legend()
    ax3.grid(True)
    
    # Error plot
    ax4 = fig.add_subplot(gs[2, :])
    line_err, = ax4.plot([], [], 'g-')
    ax4.set_xlim(0, window)
    ax4.set_ylim(0, 15)
    ax4.set_title('Prediction Error Over Time')
    ax4.set_ylabel('Error (N)')
    ax4.set_xlabel('Frame')
    ax4.grid(True)
    
    # Buffers
    fx_actual_buf, fx_pred_buf = [], []
    fy_actual_buf, fy_pred_buf = [], []
    error_buf = []
    
    # Update function
    def update(frame):
        fx_a, fy_a = actual_force[frame]
        fx_p, fy_p = pred_force[frame]
        activation = muscle_data[frame]
        
        # Arm movement vectors
        arm_line_actual.set_data([0, fx_a], [0, fy_a])
        arm_line_pred.set_data([0, fx_p], [0, fy_p])
        
        # Muscle activation
        for bar, val in zip(bars, activation):
            bar.set_height(val)
        
        # Update force buffers
        fx_actual_buf.append(fx_a)
        fx_pred_buf.append(fx_p)
        fy_actual_buf.append(fy_a)
        fy_pred_buf.append(fy_p)
        error_buf.append(np.linalg.norm([fx_a - fx_p, fy_a - fy_p]))
        
        for buf in [fx_actual_buf, fx_pred_buf, fy_actual_buf, fy_pred_buf, error_buf]:
            if len(buf) > window:
                del buf[0]
        
        line_fx_actual.set_data(range(len(fx_actual_buf)), fx_actual_buf)
        line_fx_pred.set_data(range(len(fx_pred_buf)), fx_pred_buf)
        line_fy_actual.set_data(range(len(fy_actual_buf)), fy_actual_buf)
        line_fy_pred.set_data(range(len(fy_pred_buf)), fy_pred_buf)
        line_err.set_data(range(len(error_buf)), error_buf)
        
        # Return all artists as a list
        return list(bars) + [arm_line_actual, arm_line_pred, line_fx_actual, line_fx_pred, line_fy_actual, line_fy_pred, line_err]
    
    ani = animation.FuncAnimation(fig, update, frames=len(actual_force), interval=interval, blit=False)
    plt.tight_layout()
    
    # Return the HTML animation
    return HTML(ani.to_jshtml())