from typing import Literal

# Not only literals, but typehints in General...

cursor = Literal["arrow","man","based_arrow_down","middlebutton",'based_arrow_up', 'mouse', 'boat', 'pencil', 'bogosity', 'pirate', 'bottom_left_corner', 'plus', 'bottom_right_corner', 'question_arrow', 'bottom_side', 'right_ptr', 'bottom_tee', 'right_side', 'box_spiral', 'right_tee', 'center_ptr', 'rightbutton', 'circle', 'rtl_logo', 'clock', 'sailboat', 'coffee_mug', 'sb_down_arrow', 'cross', 'sb_h_double_arrow', 'cross_reverse', 'sb_left_arrow', 'crosshair', 'sb_right_arrow', 'diamond_cross', 'sb_up_arrow', 'dot', 'sb_v_double_arrow', 'dotbox', 'shuttle', 'double_arrow', 'sizing', 'draft_large', 'spider', 'draft_small', 'spraycan', 'draped_box', 'star', 'exchange', 'target', 'fleur', 'tcross', 'gobbler', 'top_left_arrow', 'gumby', 'top_left_corner', 'hand1', 'top_right_corner', 'hand2', 'top_side', 'heart', 'top_tee', 'icon', 'trek', 'iron_cross', 'ul_angle', 'left_ptr', 'umbrella', 'left_side', 'ur_angle', 'left_tee', 'watch', 'leftbutton', 'xterm', 'll_angle', 'X_cursor', 'lr_angle']

relief = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]

padding = int|tuple[int,int]|tuple[int,int,int,int]

validate = Literal["focus","focusin","focusout","key","all","none"]

anchor = Literal["center","n","ne","e","se","s","sw","w","nw"]

bitmap = str | Literal['error', 'gray75', 'gray50', 'gray25', 'gray12', 'hourglass', 'info', 'questhead', 'question', 'warning']