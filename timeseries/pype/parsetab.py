
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '55C53B9434ED5FC68BBE31AE8D09ED67'
    
_lr_action_items = {'IMPORT':([4,],[10,]),'OP_ADD':([14,],[20,]),'OP_SUB':([14,],[27,]),'NUMBER':([7,11,12,13,15,16,18,20,21,23,25,27,29,30,31,32,33,34,36,40,41,43,44,45,46,48,52,53,54,55,56,],[13,-9,13,-27,-28,-26,-8,13,13,13,13,13,-30,13,13,13,-21,13,-11,13,-13,13,-29,-22,-24,-20,-10,-25,-12,-23,-19,]),'OP_MUL':([14,],[21,]),'LPAREN':([0,3,5,6,7,8,9,11,12,13,15,16,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,41,42,43,44,45,46,48,51,52,53,54,55,56,58,],[4,4,-4,-5,14,-2,-3,-9,14,-27,-28,-26,-8,-7,14,14,14,37,14,37,14,-6,-30,14,14,14,-21,14,-15,-11,37,-17,14,-13,37,14,-29,-22,-24,-20,-14,-10,-25,-12,-23,-19,-16,]),'STRING':([7,11,12,13,15,16,18,20,21,23,25,27,29,30,31,32,33,34,36,40,41,43,44,45,46,48,52,53,54,55,56,],[15,-9,15,-27,-28,-26,-8,15,15,15,15,15,-30,15,15,15,-21,15,-11,15,-13,15,-29,-22,-24,-20,-10,-25,-12,-23,-19,]),'ASSIGN':([14,],[22,]),'ID':([1,7,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,56,58,],[7,16,17,-9,16,-27,23,-28,-26,-8,16,16,32,16,39,16,39,16,-30,16,16,16,-21,16,-15,-11,50,39,-17,16,-13,39,16,-29,-22,-24,-20,57,-18,-14,-10,-25,-12,-23,-19,-16,]),'RBRACE':([11,12,13,15,16,18,33,36,41,45,46,48,52,53,54,55,56,],[-9,19,-27,-28,-26,-8,-21,-11,-13,-22,-24,-20,-10,-25,-12,-23,-19,]),'INPUT':([14,],[24,]),'RPAREN':([13,15,16,17,23,24,26,29,30,31,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,51,52,53,54,55,56,57,58,],[-27,-28,-26,28,33,36,41,-30,45,46,-21,48,-15,-11,52,-17,53,-13,54,55,-29,-22,-24,56,-20,-14,-10,-25,-12,-23,-19,58,-16,]),'LBRACE':([0,3,5,6,8,9,19,28,],[1,1,-4,-5,-2,-3,-7,-6,]),'OP_DIV':([14,],[25,]),'OUTPUT':([14,],[26,]),'$end':([2,3,5,6,8,9,19,28,],[0,-1,-4,-5,-2,-3,-7,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([7,12,20,21,23,25,27,30,31,32,34,40,43,],[11,18,29,29,29,29,29,44,44,47,44,44,44,]),'expression_list':([7,],[12,]),'program':([0,],[2,]),'type':([37,],[49,]),'statement_list':([0,],[3,]),'declaration':([24,26,38,42,],[35,35,51,51,]),'declaration_list':([24,26,],[38,42,]),'parameter_list':([20,21,23,25,27,],[30,31,34,40,43,]),'import_statement':([0,3,],[5,9,]),'component':([0,3,],[6,8,]),}

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
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_op_add_expression','parser.py',102),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_op_sub_expression','parser.py',107),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_op_mul_expression','parser.py',112),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_op_div_expression','parser.py',117),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',122),
  ('expression -> NUMBER','expression',1,'p_expression_num','parser.py',127),
  ('expression -> STRING','expression',1,'p_expression_str','parser.py',132),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_params_list','parser.py',137),
  ('parameter_list -> expression','parameter_list',1,'p_params_list','parser.py',138),
]
