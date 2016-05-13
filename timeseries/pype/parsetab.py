
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'E1FCB2EDDF1216D4CA039394CC93A7CE'
    
_lr_action_items = {'RBRACE':([12,13,14,15,17,28,34,39,41,44,46,50,51,52,53,55,57,],[-27,-26,-9,-28,27,-8,-13,-11,-21,-22,-12,-23,-25,-10,-20,-24,-19,]),'OP_SUB':([16,],[21,]),'NUMBER':([8,12,13,14,15,17,19,21,22,24,26,28,29,30,34,36,37,39,40,41,42,43,44,45,46,50,51,52,53,55,57,],[12,-27,-26,-9,-28,12,12,12,12,12,12,-8,12,-30,-13,12,12,-11,12,-21,12,12,-22,-29,-12,-23,-25,-10,-20,-24,-19,]),'OUTPUT':([16,],[20,]),'$end':([1,2,4,6,9,10,18,27,],[-5,0,-4,-1,-2,-3,-6,-7,]),'IMPORT':([3,],[7,]),'OP_DIV':([16,],[22,]),'STRING':([8,12,13,14,15,17,19,21,22,24,26,28,29,30,34,36,37,39,40,41,42,43,44,45,46,50,51,52,53,55,57,],[15,-27,-26,-9,-28,15,15,15,15,15,15,-8,15,-30,-13,15,15,-11,15,-21,15,15,-22,-29,-12,-23,-25,-10,-20,-24,-19,]),'RPAREN':([11,12,13,15,20,23,24,29,30,31,32,34,35,36,37,38,39,40,41,43,44,45,46,47,50,51,52,53,54,55,56,57,58,],[18,-27,-26,-28,34,39,41,44,-30,-17,46,-13,-15,50,51,52,-11,53,-21,55,-22,-29,-12,-14,-23,-25,-10,-20,57,-24,58,-19,-16,]),'ID':([5,7,8,12,13,14,15,16,17,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,58,],[8,11,13,-27,-26,-9,-28,24,13,13,31,13,13,31,13,42,13,-8,13,-30,-17,31,48,-13,-15,13,13,31,-11,13,-21,13,13,-22,-29,-12,-14,-18,56,-23,-25,-10,-20,-24,-19,-16,]),'ASSIGN':([16,],[25,]),'INPUT':([16,],[23,]),'LPAREN':([0,1,4,6,8,9,10,12,13,14,15,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,47,50,51,52,53,55,57,58,],[3,-5,-4,3,16,-2,-3,-27,-26,-9,-28,16,-6,16,33,16,16,33,16,16,-7,-8,16,-30,-17,33,-13,-15,16,16,33,-11,16,-21,16,16,-22,-29,-12,-14,-23,-25,-10,-20,-24,-19,-16,]),'OP_MUL':([16,],[26,]),'LBRACE':([0,1,4,6,9,10,18,27,],[5,-5,-4,5,-2,-3,-6,-7,]),'OP_ADD':([16,],[19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'component':([0,6,],[1,9,]),'parameter_list':([19,21,22,24,26,],[29,36,37,40,43,]),'program':([0,],[2,]),'type':([33,],[49,]),'declaration_list':([20,23,],[32,38,]),'expression':([8,17,19,21,22,24,26,29,36,37,40,42,43,],[14,28,30,30,30,30,30,45,45,45,45,54,45,]),'import_statement':([0,6,],[4,10,]),'expression_list':([8,],[17,]),'statement_list':([0,],[6,]),'declaration':([20,23,32,38,],[35,35,47,47,]),}

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
