for rec in records:

	obj_ap = env['account.payment']
	obj_apm = env['account.payment.method']
	
	if rec.state != 'paid':
		raise Warning("Registro(s) com status diferente de pago foram selecionados.\n Operação não permitida!")
	
	if not rec.invoice_id:
		raise Warning("Registro(s) sem fatura de origem.\n Operação não permitida!")
	
	if rec.invoice_id.payment_ids:
		raise Warning("Registro(s) com pagamentos efetuados em fatura de origem foram selecionados.\n Operação não permitida!")
	
	cpn_pol = rec.company_id.id
	vfn_pol = rec.value_final
	ivc_pol	= rec.invoice_id.id
	jnl_pol = rec.journal_id.id
	ptn_pol = rec.partner_id.id
	ctm_pol	= "customer"
	ivn_pol = rec.invoice_id.number
	inb_pol = "inbound"

	for reconciled_line in rec.move_line_id.full_reconcile_id.reconciled_line_ids:
		if reconciled_line.credit > 0:
		  reconciled_line_credit = reconciled_line

	name_pol = reconciled_line_credit.move_id.name

	if rec.payment_date:
		pymd_pol = rec.payment_date
	else:
		pymd_pol = reconciled_line_credit.move_id.date

	elec_pol = obj_apm.search([('code', '=', 'electronic')]).id

	add_fields =	{
					'company_id': cpn_pol,
					'amount': vfn_pol,
					'journal_id': jnl_pol,
					'partner_id': ptn_pol,
					'partner_type': ctm_pol,
					'communication': ivn_pol,
					'payment_type': inb_pol,
					'move_name': name_pol,
					'payment_date': pymd_pol,
					'payment_method_id': elec_pol,
					'invoice_ids': [(6, 0, [ivc_pol])]
					}				
	
	create_payment = obj_ap.create(add_fields)

	for mv_ln in reconciled_line_credit.move_id.line_ids:
		mv_ln.write({'payment_id': create_payment.id})