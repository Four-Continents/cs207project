
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '9DBB5F0341783F8E01DA72239FEDDC11'
    
_lr_action_items = {'LPAREN':([11,],[21,]),'RPAREN':([21,],[30,]),'RBRACK':([15,16,34,],[25,-13,-12,]),'NUMBER':([1,7,19,26,39,44,],[5,16,28,34,43,45,]),'AT':([6,25,],[14,-11,]),'AS':([30,],[36,]),'FROM':([4,9,10,11,12,31,32,42,],[8,-17,18,-18,-14,-16,-18,-15,]),'COMMA':([9,11,12,15,16,31,32,34,42,],[-17,-18,22,26,-13,-16,-18,-12,22,]),'INSERT':([0,],[2,]),'LBRACK':([2,14,],[7,7,]),'ASC':([35,],[38,]),'$end':([3,9,10,11,12,17,23,27,28,31,32,35,37,38,40,41,42,43,45,],[0,-17,-4,-18,-14,-2,-10,-3,-5,-16,-18,-6,-1,-19,-20,-7,-15,-8,-9,]),'INTO':([24,25,],[33,-11,]),'DESC':([35,],[40,]),'BY':([20,],[29,]),'LIKE':([5,],[13,]),'LIMIT':([9,10,11,12,31,32,35,38,40,41,42,],[-17,19,-18,-14,-16,-18,39,-19,-20,44,-15,]),'SELECT':([0,],[4,]),'ID':([4,8,13,18,22,29,33,36,],[11,17,23,27,32,35,37,32,]),'SIMSEARCH':([0,],[1,]),'ORDER':([9,10,11,12,31,32,42,],[-17,20,-18,-14,-16,-18,-15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'field_name':([4,22,36,],[9,31,9,]),'bracketed_number_list':([2,14,],[6,24,]),'number_list':([7,],[15,]),'selector':([4,],[10,]),'order_direction':([35,],[41,]),'field_list':([4,36,],[12,42,]),'command':([0,],[3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> command","S'",1,None,None,None),
  ('command -> INSERT bracketed_number_list AT bracketed_number_list INTO ID','command',6,'p_insert_command','parser.py',8),
  ('command -> SELECT FROM ID','command',3,'p_select_from','parser.py',13),
  ('command -> SELECT selector FROM ID','command',4,'p_select_from','parser.py',14),
  ('command -> SELECT selector','command',2,'p_select_multi','parser.py',25),
  ('command -> SELECT selector LIMIT NUMBER','command',4,'p_select_multi','parser.py',26),
  ('command -> SELECT selector ORDER BY ID','command',5,'p_select_multi','parser.py',27),
  ('command -> SELECT selector ORDER BY ID order_direction','command',6,'p_select_multi','parser.py',28),
  ('command -> SELECT selector ORDER BY ID LIMIT NUMBER','command',7,'p_select_multi','parser.py',29),
  ('command -> SELECT selector ORDER BY ID order_direction LIMIT NUMBER','command',8,'p_select_multi','parser.py',30),
  ('command -> SIMSEARCH NUMBER LIKE ID','command',4,'p_simsearch','parser.py',49),
  ('bracketed_number_list -> LBRACK number_list RBRACK','bracketed_number_list',3,'p_bracketed_number_list','parser.py',58),
  ('number_list -> number_list COMMA NUMBER','number_list',3,'p_number_list','parser.py',63),
  ('number_list -> NUMBER','number_list',1,'p_number_list','parser.py',64),
  ('selector -> field_list','selector',1,'p_selector','parser.py',74),
  ('selector -> ID LPAREN RPAREN AS field_list','selector',5,'p_selector','parser.py',75),
  ('field_list -> field_list COMMA field_name','field_list',3,'p_field_list','parser.py',83),
  ('field_list -> field_name','field_list',1,'p_field_list','parser.py',84),
  ('field_name -> ID','field_name',1,'p_field_name','parser.py',94),
  ('order_direction -> ASC','order_direction',1,'p_order_direction','parser.py',99),
  ('order_direction -> DESC','order_direction',1,'p_order_direction','parser.py',100),
]
