
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'B7DA2FE6C22431AB95D14A63E4FE0078'
    
_lr_action_items = {'OP_SUB':([12,],[20,]),'LBRACE':([0,1,3,4,8,9,18,28,],[2,-5,2,-4,-2,-3,-7,-6,]),'RPAREN':([13,14,16,17,22,23,24,29,30,31,32,33,34,35,37,38,39,40,41,43,44,45,46,47,48,51,52,53,54,55,56,57,58,],[-27,-26,-28,28,35,38,39,-30,44,46,-17,48,-15,-11,51,-13,-21,52,53,55,-23,-29,-22,-14,-10,-12,-20,-24,57,-25,58,-19,-16,]),'OP_ADD':([12,],[21,]),'IMPORT':([5,],[10,]),'LPAREN':([0,1,3,4,7,8,9,11,13,14,15,16,18,19,20,21,22,23,24,25,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,48,51,52,53,55,57,58,],[5,-5,5,-4,12,-2,-3,12,-27,-26,-9,-28,-7,-8,12,12,36,36,12,12,12,-6,-30,12,12,-17,36,-15,-11,36,-13,-21,12,12,12,12,-23,-29,-22,-14,-10,-12,-20,-24,-25,-19,-16,]),'RBRACE':([11,13,14,15,16,19,35,38,39,44,46,48,51,52,53,55,57,],[18,-27,-26,-9,-28,-8,-11,-13,-21,-23,-22,-10,-12,-20,-24,-25,-19,]),'INPUT':([12,],[22,]),'OUTPUT':([12,],[23,]),'ID':([2,7,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,58,],[7,14,17,14,24,-27,-26,-9,-28,-8,14,14,32,32,14,14,42,14,-30,14,14,-17,32,-15,-11,50,32,-13,-21,14,14,14,14,-23,-29,-22,-14,-10,56,-18,-12,-20,-24,-25,-19,-16,]),'OP_MUL':([12,],[25,]),'NUMBER':([7,11,13,14,15,16,19,20,21,24,25,27,29,30,31,35,38,39,40,41,42,43,44,45,46,48,51,52,53,55,57,],[13,13,-27,-26,-9,-28,-8,13,13,13,13,13,-30,13,13,-11,-13,-21,13,13,13,13,-23,-29,-22,-10,-12,-20,-24,-25,-19,]),'$end':([1,3,4,6,8,9,18,28,],[-5,-1,-4,0,-2,-3,-7,-6,]),'ASSIGN':([12,],[26,]),'OP_DIV':([12,],[27,]),'STRING':([7,11,13,14,15,16,19,20,21,24,25,27,29,30,31,35,38,39,40,41,42,43,44,45,46,48,51,52,53,55,57,],[16,16,-27,-26,-9,-28,-8,16,16,16,16,16,-30,16,16,-11,-13,-21,16,16,16,16,-23,-29,-22,-10,-12,-20,-24,-25,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'component':([0,3,],[1,8,]),'type':([36,],[49,]),'expression_list':([7,],[11,]),'expression':([7,11,20,21,24,25,27,30,31,40,41,42,43,],[15,19,29,29,29,29,29,45,45,45,45,54,45,]),'declaration':([22,23,33,37,],[34,34,47,47,]),'statement_list':([0,],[3,]),'parameter_list':([20,21,24,25,27,],[30,31,40,41,43,]),'declaration_list':([22,23,],[33,37,]),'import_statement':([0,3,],[4,9,]),'program':([0,],[6,]),}

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
  ('declaration -> LPAREN type ID RPAREN','declaration',4,'p_declaration','parser.py',74),
  ('declaration -> ID','declaration',1,'p_declaration','parser.py',75),
  ('type -> ID','type',1,'p_type','parser.py',83),
  ('expression -> LPAREN ASSIGN ID expression RPAREN','expression',5,'p_expression_assign','parser.py',88),
  ('expression -> LPAREN ID parameter_list RPAREN','expression',4,'p_expression_eval','parser.py',94),
  ('expression -> LPAREN ID RPAREN','expression',3,'p_expression_eval','parser.py',95),
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_op_add_expression','parser.py',103),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_op_sub_expression','parser.py',108),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_op_mul_expression','parser.py',113),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_op_div_expression','parser.py',118),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',123),
  ('expression -> NUMBER','expression',1,'p_expression_num','parser.py',128),
  ('expression -> STRING','expression',1,'p_expression_str','parser.py',133),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_params_list','parser.py',138),
  ('parameter_list -> expression','parameter_list',1,'p_params_list','parser.py',139),
]
