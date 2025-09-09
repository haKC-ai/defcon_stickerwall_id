import fade

BANNER_LOGO = """
              ▒█████████▒               
             █████████████             
            ███   ███   ███            
    ████   ████   ███   ████    ▓▓     
    ▓██░  ░██ ▒█████████░ ██   ████    
  ░███████░██ ██████████▒ ██   █████   
   ██▒ ▓██████ ▒███████  ███████████▓  
           ██████     ███████▒         
              ███████████▓             
                 ▓█████                
            ██████   █████▒            
    ▒███▒█████░         ▓█████▓██▒     
     █████▒                ░█████      
      ████                   ███       
       ██                    ██        
"""
BANNER_DEF = """





░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░        
"""

BANNER_CON = """





  ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░
"""                           

def print_banner_side_by_side():
    banners = [
        fade.greenblue(BANNER_LOGO),
        fade.purplepink(BANNER_DEF),
        fade.purplepink(BANNER_CON).strip()       
    ]

    all_lines = [b.strip().splitlines() for b in banners]
    widths = [max(len(line) for line in banner_lines) if banner_lines else 0 for banner_lines in all_lines]
    max_height = max(len(banner_lines) for banner_lines in all_lines) if all_lines else 0

    print("\n")
    for i in range(max_height):
        row_parts = []
        for j, banner_lines in enumerate(all_lines):
            line = banner_lines[i] if i < len(banner_lines) else ""
            padded_line = line.ljust(widths[j])
            row_parts.append(padded_line)
        print("  ".join(row_parts))