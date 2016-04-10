
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'E1FCB2EDDF1216D4CA039394CC93A7CE'
    
_lr_action_items = {'ASSIGN':([12,],[19,]),'LPAREN':([0,1,2,3,7,8,10,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,45,46,47,50,51,52,53,54,55,56,58,],[4,-4,4,-5,-3,-2,12,-26,-27,12,-9,-28,-6,12,12,36,12,36,12,12,-8,-7,12,12,-30,-21,12,-15,-17,-11,36,12,-13,36,12,12,-29,-20,-24,-14,-10,-25,-12,-23,-22,-19,-16,]),'ID':([5,9,10,12,13,14,15,16,17,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,],[10,11,13,20,-26,-27,13,-9,-28,29,13,13,35,13,35,13,13,-8,13,13,-30,-21,13,-15,-17,49,-11,35,13,-13,35,13,13,-29,-20,-24,57,-18,-14,-10,-25,-12,-23,-22,-19,-16,]),'OP_ADD':([12,],[26,]),'RPAREN':([11,13,14,17,20,22,24,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,58,],[18,-26,-27,-28,32,37,40,46,-30,-21,47,-15,-17,-11,51,52,-13,53,54,55,56,-29,-20,-24,-14,-10,-25,-12,-23,-22,-19,58,-16,]),'OP_MUL':([12,],[21,]),'INPUT':([12,],[22,]),'NUMBER':([10,13,14,15,16,17,20,21,23,25,26,27,29,30,31,32,33,37,39,40,42,43,45,46,47,51,52,53,54,55,56,],[14,-26,-27,14,-9,-28,14,14,14,14,14,-8,14,14,-30,-21,14,-11,14,-13,14,14,-29,-20,-24,-10,-25,-12,-23,-22,-19,]),'STRING':([10,13,14,15,16,17,20,21,23,25,26,27,29,30,31,32,33,37,39,40,42,43,45,46,47,51,52,53,54,55,56,],[17,-26,-27,17,-9,-28,17,17,17,17,17,-8,17,17,-30,-21,17,-11,17,-13,17,17,-29,-20,-24,-10,-25,-12,-23,-22,-19,]),'$end':([1,2,3,6,7,8,18,28,],[-4,-1,-5,0,-3,-2,-6,-7,]),'OP_SUB':([12,],[25,]),'OUTPUT':([12,],[24,]),'LBRACE':([0,1,2,3,7,8,18,28,],[5,-4,5,-5,-3,-2,-6,-7,]),'OP_DIV':([12,],[23,]),'RBRACE':([13,14,15,16,17,27,32,37,40,46,47,51,52,53,54,55,56,],[-26,-27,28,-9,-28,-8,-21,-11,-13,-20,-24,-10,-25,-12,-23,-22,-19,]),'IMPORT':([4,],[9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'import_statement':([0,2,],[1,7,]),'statement_list':([0,],[2,]),'component':([0,2,],[3,8,]),'expression':([10,15,20,21,23,25,26,29,30,33,39,42,43,],[16,27,31,31,31,31,31,44,45,45,45,45,45,]),'declaration':([22,24,38,41,],[34,34,50,50,]),'type':([36,],[48,]),'parameter_list':([20,21,23,25,26,],[30,33,39,42,43,]),'program':([0,],[6,]),'expression_list':([10,],[15,]),'declaration_list':([22,24,],[38,41,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',8),
  ('statement_list -> statement_list component','statement_list',2,'p_statement_list','parser.py',14),
  ('statement_list -> statement_list import_statement','statement_list',2,'p_statement_list','parser.py',15),
  ('statement_list -> import_statement','statement_list',1,'p_statement_list','parser.py',16),
  ('statement_list -> component','statement_list',1,'p_statement_list','parser.py',17),
  ('import_statement -> LPAREN IMPORT ID RPAREN','import_statement',4,'p_import_statement','parser.py',26),
  ('component -> LBRACE ID expression_list RBRACE','component',4,'p_component','parser.py',31),
  ('expression_list -> expression_list expression','expression_list',2,'p_expression_list','parser.py',36),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',37),
  ('expression -> LPAREN INPUT declaration_list RPAREN','expression',4,'p_expression_input','parser.py',46),
  ('expression -> LPAREN INPUT RPAREN','expression',3,'p_expression_input','parser.py',47),
  ('expression -> LPAREN OUTPUT declaration_list RPAREN','expression',4,'p_expression_output','parser.py',55),
  ('expression -> LPAREN OUTPUT RPAREN','expression',3,'p_expression_output','parser.py',56),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list','parser.py',64),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','parser.py',65),
  ('declaration -> LPAREN type ID RPAREN','declaration',4,'p_declaration','parser.py',73),
  ('declaration -> ID','declaration',1,'p_declaration','parser.py',74),
  ('type -> ID','type',1,'p_type','parser.py',82),
  ('expression -> LPAREN ASSIGN ID expression RPAREN','expression',5,'p_expression_assign','parser.py',87),
  ('expression -> LPAREN ID parameter_list RPAREN','expression',4,'p_expression_eval','parser.py',93),
  ('expression -> LPAREN ID RPAREN','expression',3,'p_expression_eval','parser.py',94),
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_expression_add','parser.py',102),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_expression_subtract','parser.py',107),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_expression_mult','parser.py',112),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_expression_div','parser.py',117),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',122),
  ('expression -> NUMBER','expression',1,'p_expression_num','parser.py',127),
  ('expression -> STRING','expression',1,'p_expression_str','parser.py',132),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_params_list','parser.py',137),
  ('parameter_list -> expression','parameter_list',1,'p_params_list','parser.py',138),
]
