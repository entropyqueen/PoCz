%define	BUFFSIZE 32768

	section .text
	global _start

;;; Strlen
len:
	xor rax, rax
len_beg:
	cmp byte [rdi + rax], 0
	je len_end
	inc rax
	jmp len_beg
len_end:
	ret

;;; my_putstr
pstr:
	call len
	mov rdx, rax
	mov rsi, rdi
	mov rax, 1
	mov rdi, 1
	syscall
	ret

;;; my_cat
cat:
	push rbp
	mov rbp, rsp
	cmp r13, 0
	je read_stdin
	mov rax, 2
	mov rsi, 0
	syscall			; Open file
	cmp rax, 0
	jl cat_error
	mov r15, rax
	jmp read
read_stdin:
	mov r15, 0
read:
	mov rdi, r15
	mov rax, 0
	mov rsi, buff
	mov rdx, BUFFSIZE
	syscall
	cmp rax, 0
	jle cat_end		; If read returns 0, jump to end.
	mov byte [rsi + rax], 0	; write a \0 at the end of the string.
	mov rdi, rsi
	call pstr 		; Writing buffer to stdout
	jmp read		; And here we go again 'til read returns 0
cat_close:
	cmp r13, 0
	je cat_end
	mov rdi, r15
	mov rax, 3
	syscall
	jmp cat_end
cat_error:
	mov rdi, openerr
	call pstr
cat_end:
	leave
	ret

;;; Travels across the args
args_t:
	push rbp
	mov rbp, rsp
	xor r10, r10
	dec r9
_args_t_b:
	mov rdi, [rbp + 24 + 8 * r10]
	cmp r10, r9
	jge _args_t_e
	push r9
	call cat
	inc r10
	pop r9
	jmp _args_t_b
_args_t_e:
	leave
	ret

nofile:
	xor r13, r13
	call cat
	jmp end

;;; Entry point
_start:
	pop r9
	cmp r9, 2
	jl nofile
	mov r13, 1
	call args_t
end:
	xor rdi, rdi
	mov rax, 60
	syscall

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	section .data		;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
nl	db 10, 0
openerr db 'Failed to open file', 10, 0

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	section .bss 		;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
buff	resb BUFFSIZE
