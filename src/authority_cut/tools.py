from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from threading import RLock
from typing import Any

@dataclass
class VendorTools:
    conn: sqlite3.Connection
    lock: RLock

    @classmethod
    def memory(cls):
        conn=sqlite3.connect(':memory:', check_same_thread=False)
        conn.execute('create table vendor(id text primary key, name text, tax_status text, bank_status text, state text)')
        conn.execute('create table effects(action_id text primary key, kind text, payload text, compensated integer default 0)')
        return cls(conn, RLock())

    def execute(self,tool:str,payload:dict[str,Any])->dict[str,Any]:
        with self.lock:
            vid=payload.get('vendor_id','V-42')
            if tool=='collect_vendor_record': return {'vendor_id':vid,'name':'Acme Components','source':'vendor_portal'}
            if tool=='validate_tax_id': return {'vendor_id':vid,'tax_status':'EXCEPTION_NAME_VARIANT','evidence':'tax-check-42'}
            if tool=='validate_bank': return {'vendor_id':vid,'bank_status':'NEW_ACCOUNT','evidence':'bank-check-42'}
            if tool=='create_draft_vendor':
                self.conn.execute("insert or replace into vendor values(?,?,?,?,?)",(vid,'Acme Components','EXCEPTION_NAME_VARIANT','NEW_ACCOUNT','DRAFT')); self.conn.commit(); return {'vendor_id':vid,'state':'DRAFT'}
            if tool=='schedule_followup':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'reminder','scheduled')); self.conn.commit(); return {'scheduled':True}
            if tool=='activate_vendor':
                self.conn.execute("update vendor set state='ACTIVE' where id=?",(vid,)); self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'activation','ACTIVE')); self.conn.commit(); return {'vendor_id':vid,'state':'ACTIVE'}
            if tool=='sync_vendor_to_erp':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'erp_sync','SYNCED')); self.conn.commit(); return {'vendor_id':vid,'erp':'SYNCED'}
            if tool=='open_purchase_channel':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'purchase_channel','OPEN')); self.conn.commit(); return {'vendor_id':vid,'purchase_channel':'OPEN'}
            if tool=='enable_payments':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'payment_enable','ENABLED')); self.conn.commit(); return {'vendor_id':vid,'payments':'ENABLED'}
            if tool=='set_payment_terms':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'payment_terms','NET_30')); self.conn.commit(); return {'vendor_id':vid,'terms':'NET_30'}
            if tool=='prepare_remittance_profile':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'remittance','PREPARED')); self.conn.commit(); return {'vendor_id':vid,'remittance':'PREPARED','evidence':'remittance-preview-42'}
            if tool=='transmit_first_payment':
                self.conn.execute("insert or replace into effects(action_id,kind,payload) values(?,?,?)",(payload['action_id'],'funds_transfer','TRANSMITTED')); self.conn.commit(); return {'vendor_id':vid,'first_payment':'TRANSMITTED'}
            raise ValueError(tool)

    def compensate(self,tool:str,payload:dict[str,Any])->dict[str,Any]:
        with self.lock:
            vid=payload.get('vendor_id','V-42')
            if tool=='activate_vendor': self.conn.execute("update vendor set state='DRAFT' where id=?",(vid,))
            elif tool=='schedule_followup': pass
            elif tool in {'enable_payments','sync_vendor_to_erp','open_purchase_channel','set_payment_terms','prepare_remittance_profile'}:
                self.conn.execute("update effects set compensated=1 where action_id=?",(payload['action_id'],))
            else: raise ValueError(f'no compensation for {tool}')
            self.conn.execute("update effects set compensated=1 where action_id=?",(payload['action_id'],)); self.conn.commit()
            return {'compensated':True,'action_id':payload['action_id']}
