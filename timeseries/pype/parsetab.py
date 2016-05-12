
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '371EF72B57DF7D01BB0A145AD73D5ADC'
    
_lr_action_items = {'OP_SUB':([14,],[20,]),'RPAREN':([11,13,15,17,19,23,24,30,31,32,33,34,35,36,38,39,40,41,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,],[18,-28,-26,-27,30,39,40,-13,-15,46,-17,48,-30,50,52,-21,-11,53,54,55,-12,-14,-23,-29,-24,57,-20,-10,-22,-25,58,-19,-16,]),'OUTPUT':([14,],[19,]),'RBRACE':([12,13,15,16,17,27,30,39,40,46,48,50,52,53,54,55,57,],[-9,-28,-26,28,-27,-8,-13,-21,-11,-12,-23,-24,-20,-10,-22,-25,-19,]),'LBRACE':([0,2,3,4,8,9,18,28,],[5,5,-5,-4,-2,-3,-6,-7,]),'STRING':([10,12,13,15,16,17,20,21,23,25,26,27,30,34,35,36,37,38,39,40,42,43,46,48,49,50,52,53,54,55,57,],[13,-9,-28,-26,13,-27,13,13,13,13,13,-8,-13,13,-30,13,13,13,-21,-11,13,13,-12,-23,-29,-24,-20,-10,-22,-25,-19,]),'OP_ADD':([14,],[25,]),'ASSIGN':([14,],[22,]),'LPAREN':([0,2,3,4,8,9,10,12,13,15,16,17,18,19,20,21,23,24,25,26,27,28,30,31,32,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,50,52,53,54,55,57,58,],[1,1,-5,-4,-2,-3,14,-9,-28,-26,14,-27,-6,29,14,14,14,29,14,14,-8,-7,-13,-15,29,-17,14,-30,14,14,14,-21,-11,29,14,14,-12,-14,-23,-29,-24,-20,-10,-22,-25,-19,-16,]),'ID':([5,7,10,12,13,14,15,16,17,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,57,58,],[10,11,15,-9,-28,23,-26,15,-27,33,15,15,37,15,33,15,15,-8,44,-13,-15,33,-17,15,-30,15,15,15,-21,-11,33,15,15,-18,56,-12,-14,-23,-29,-24,-20,-10,-22,-25,-19,-16,]),'INPUT':([14,],[24,]),'OP_MUL':([14,],[21,]),'NUMBER':([10,12,13,15,16,17,20,21,23,25,26,27,30,34,35,36,37,38,39,40,42,43,46,48,49,50,52,53,54,55,57,],[17,-9,-28,-26,17,-27,17,17,17,17,17,-8,-13,17,-30,17,17,17,-21,-11,17,17,-12,-23,-29,-24,-20,-10,-22,-25,-19,]),'OP_DIV':([14,],[26,]),'IMPORT':([1,],[7,]),'$end':([2,3,4,6,8,9,18,28,],[-1,-5,-4,0,-2,-3,-6,-7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'parameter_list':([20,21,23,25,26,],[34,36,38,42,43,]),'declaration':([19,24,32,41,],[31,31,47,47,]),'statement_list':([0,],[2,]),'component':([0,2,],[3,8,]),'expression':([10,16,20,21,23,25,26,34,36,37,38,42,43,],[12,27,35,35,35,35,35,49,49,51,49,49,49,]),'import_statement':([0,2,],[4,9,]),'type':([29,],[45,]),'program':([0,],[6,]),'expression_list':([10,],[16,]),'declaration_list':([19,24,],[32,41,]),}

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
